---
name: context-bootstrap
description: >-
  Reference and governance authority for the bootstrap session-continuity
  protocol. Defines schema, naming convention, project-relative storage,
  task carry-forward matrix, session-scoped decision rules, operator-driven
  selection dialog, recovery protocol, archive housekeeping, and anti-drift
  policy. Use this command for questions about bootstrap structure, schema
  fields, naming conventions, carry-forward rules, recovery flow, or
  bootstrap governance. Procedural execution of bootstrap phases (ingest,
  audit, init, checkpoint, finalize) is NOT handled here — those are
  separate commands defined in the commands/ directory.
---

```yaml
command: context-bootstrap
type: governance_and_schema
procedural_execution: deferred_to_commands

architecture:
  layers:
    governance:
      owner: this_command
      files: [COMMAND.md, schema.yaml, example-bootstrap.yaml]
      responsibility: [schema, naming, carry_forward_matrix, decision_rules, recovery_protocol, archive_housekeeping, anti_drift, error_policy]
    procedure:
      owner: commands
      files: [commands/manifest.yaml, commands/bootstrap-*.yaml]
      responsibility: [atomic_phase_execution]

commands:
  bootstrap-start:
    type: macro
    when: session_start
    chains: [bootstrap-ingest, bootstrap-audit, bootstrap-init]
  bootstrap-ingest:
    type: atomic
    phase: 1.1
    when: session_start
  bootstrap-audit:
    type: atomic
    phase: 1.2
    when: after_ingest
  bootstrap-init:
    type: atomic
    phase: 1.3
    when: after_audit
  bootstrap-checkpoint:
    type: atomic
    phase: 2.4
    when: [event_trigger, manual, periodic_self_check]
  bootstrap-finalize:
    type: atomic
    phase: 3.5
    when: session_end

bootstrap_definition:
  is:
    - single_yaml_file
    - captures_complete_working_state_at_session_end
    - sole_mechanism_for_inter_session_context_transfer
    - one_per_session
    - documents_only_what_its_session_did
  is_not:
    - changelog_or_journal
    - conversation_summary
    - optional
    - storage_for_agent_thoughts
    - accumulating_history_of_all_prior_decisions

storage:
  live_path: "{project_root}/02_working/chat-sessions/bootstrap/"
  archive_path: "{project_root}/02_working/chat-sessions/bootstrap/_ar/"  # deferred only; commands must not create/use while archive_housekeeping.status starts with DEFERRED
  project_root_format: absolute_path_only
  project_root_source: operator_supplied
  pattern_scope: project_agnostic_applies_to_all_projects

naming:
  pattern: "{ProjectName}_{YYMMDD-HHMM}.yaml"
  timestamp_basis: session_end_time
  revision_suffixes: forbidden
  retention: project_lifetime
  supplemental_pattern: "{ProjectName}_{BrokenSessionID}S.yaml"
  supplemental_marker: top_level_supplemental_field_set_to_true
  immutability:
    older_files: read_only
    modification: forbidden
  examples:
    - TransLineEstimator_260318-1430.yaml
    - PDKOS_260319-0900.yaml
    - FormBuilder_260402-2145.yaml
    - Utilix_260428-1731S.yaml  # supplemental for broken Utilix_260428-1731

session_start_dialog:
  authority: bootstrap-start_macro
  principle: operator_driven_never_autonomous
  paths:
    path_1_specific_bootstrap_supplied:
      trigger: operator_passes_explicit_path_or_at_reference_to_prior_bootstrap_yaml
      action: use_supplied_path_directly_derive_project_root_by_fourth_parent_above_file
      then: invoke_ingest
    path_2_existing_project_no_specific_bootstrap:
      trigger: operator_indicates_existing_project_root_only
      action_sequence:
        - prompt_or_confirm_project_root_absolute_path
        - run_lock_check
        - inspect_live_dir_for_canonical_bootstraps
        - if_multiple_list_all_let_operator_choose
        - if_one_propose_candidate_per_Q1_wording_and_await_confirmation
        - if_zero_ask_operator_session_zero_or_halt
      Q1_wording: "Found {filename} (session {session_id}, ended {iso_timestamp}). Continue this session?"
      Q3_multiple_loose_files: list_all_let_operator_choose
      Q0_zero_candidates: "No canonical bootstrap found under {project_root}/02_working/chat-sessions/bootstrap/. Start session-zero for this project?"
      then: invoke_ingest
    path_3_session_zero:
      trigger: operator_declares_new_project_or_no_prior_bootstrap_exists
      action_sequence:
        - prompt_for_project_name
        - prompt_for_project_root_absolute_path_per_Q4
        - set_session_zero_flag
      then: skip_ingest_invoke_init_directly
  hard_rule: agent_NEVER_auto_selects_a_bootstrap_halt_preferred_over_guessing

recovery_protocol:
  authority: bootstrap-ingest_command
  principle: broken_or_missing_bootstrap_is_first_class_flow_not_session_killer
  scenarios:
    scenario_2_1_broken_bootstrap:
      definition_per_Q7: yaml_parse_failure_OR_schema_validation_failure_OR_data_integrity_failure
      flow:
        - id: R3_review_partial
          action: read_broken_file_as_raw_text_extract_recoverable_sections
          notes: top_of_file_identity_block_usually_intact
        - id: R5_archive_recovery
          status: DEFERRED_WHILE_ARCHIVE_HOUSEKEEPING_DEFERRED
          action_sequence:
            - pull_most_recent_bootstrap_from_live_dir_archive
            - perform_360_review_using_all_available_bootstraps
            - generate_line_by_line_status_report_on_previous_open_items
            - generate_supplemental_bootstrap
        - id: R5_live_dir_recovery
          status: ACTIVE_WHILE_ARCHIVE_HOUSEKEEPING_DEFERRED
          action_sequence:
            - inspect_loose_canonical_bootstraps_in_live_dir
            - exclude_broken_file_and_supplemental_derivatives_unless_operator_selected
            - choose_most_recent_valid_candidate_by_filename_timestamp_then_session_ended_then_file_modified
            - perform_360_review_using_all_available_live_dir_bootstraps
            - generate_line_by_line_status_report_on_previous_open_items
            - generate_supplemental_bootstrap
        - id: R6_broken_file_disposal
          action: send_broken_file_to_OS_desktop_recycle_bin_after_supplemental_verified
          authority: housekeeping_command_removal_flow
          condition: supplemental_must_be_written_and_verified_first
    scenario_2_2_stale_lock_present:
      flow:
        - prompt_operator_lock_present_remove_or_halt
        - on_YES_remove_lock_check_for_corresponding_bootstrap
        - on_YES_no_bootstrap_exists_dispatch_to_recovery_scenario_2_1
        - on_NO_halt_entirely_per_Q5
      hard_rule: operator_manually_closes_out_next_session_re_runs_same_checks
  no_valid_recovery_candidate_fallback_per_Q6:
    trigger: recovery_needed_but_live_dir_has_no_valid_recovery_candidate
    action: ask_operator_confirm_session_zero_then_fall_through_to_init_using_known_project_root_and_project_name
    carry_forward: none
  supplemental_bootstrap:
    naming_per_Q8_2: "{ProjectName}_{BrokenSessionID}S.yaml"
    location_per_Q8_1: same_live_dir_as_canonical_bootstraps
    schema_marker:
      supplemental: true
      supersedes: broken_session_id

archive_housekeeping:
  status: DEFERRED_PENDING_FSA_LONG_TERM_STORAGE_FINALIZATION
  active_boundary: commands_MUST_NOT_execute_archive_housekeeping_while_status_starts_with_DEFERRED
  status_note: >-
    DEFERRED by prior storage-authority decision. Bootstraps
    currently remain LOOSE under {live_path} with no _ar/ sibling and no
    date-zip rollup. Spec preserved for activation when long-term storage
    finalization lands through a separate approved decision. Until reactivated:
    bootstrap-finalize does not implement this section, bootstrap-init does
    not create the _ar/ sibling, and old-path one-time migration is complete.
  authority: bootstrap-finalize_command
  principle: keep_live_dir_clean_while_preserving_full_history
  trigger: every_finalize_after_current_bootstrap_written_and_verified
  algorithm:
    - id: 1_group_loose_bootstraps_by_date
      scope: live_dir_yaml_files_EXCEPT_just_written_current_one
      key: YYMMDD_prefix_in_filename
    - id: 2_zip_per_date
      destination: "{archive_path}/{YYMMDD}.zip"
      collision_behavior: merge_new_files_into_existing_zip
      forbidden: zip_files_of_different_dates_together
    - id: 3_verify_then_delete_originals
      action: send_zipped_originals_to_OS_desktop_recycle_bin_after_zip_verified
      authority: housekeeping_command_removal_flow
  date_determination_priority:
    - filename_embedded_date_YYMMDD-HHMM_token
    - yaml_internal_session_started_field_date
    - file_system_modified_date
  out_of_scope:
    - just_written_current_bootstrap_stays_loose
    - non_bootstrap_files_in_live_dir
    - non_yaml_files
  one_time_migration:
    trigger: first_finalize_after_protocol_overhaul_when_OLD_path_still_has_bootstraps
    OLD_path: "{project_root}/bootstrap/"
    action: date_zip_OLD_path_bootstraps_into_new_archive_path_then_recycle_bin_originals
    out_of_scope: non_bootstrap_files_in_OLD_path_stay_put

task_carry_forward_matrix:
  authority_corpus_file: corpus/charter--1a017eabb2e8.yaml
  authority_block: payload.session_continuity_vocabulary.task_carry_forward_matrix
  status_note: >-
    Vocabulary parked in charter as TEMPORARY_TENANT pending creation of a
    dedicated corpus envelope (bootstrap-vocabulary--{shortUUID}.yaml).
    See payload.session_continuity_vocabulary.todo in the charter.
  enforcement: corpus_block_is_authoritative_command_must_not_redefine

task_id_rules:
  format: "T-NNN"
  permanence: id_is_permanent_within_origin_session_not_propagated_after_DONE
  reuse: forbidden
  assignment: next_available_integer

task_ordering:
  basis: deterministic_three_key_sort
  keys:
    - {priority: 1, field: status, order: [ACTIVE, BLOCKED, DEFERRED]}
    - {priority: 2, field: priority, order: [HIGH, MEDIUM, LOW]}
    - {priority: 3, field: id, order: ascending}
  consistency: must_be_identical_within_a_bootstrap

decision_logging:
  trigger: any_choice_made_THIS_session_that_could_reasonably_go_differently
  scope:
    log:
      - project_direction
      - architecture
      - naming
      - scope
      - tooling
      - approach
    do_not_log:
      - trivial_operational_choices
      - implementation_micro_details
  permanence:
    scope: session_of_origin_only
    carry_forward: false
    rationale: bootstrap_documents_what_session_did_not_full_project_history
    long_term_archival: corpus_responsibility_not_bootstrap
  zero_context_test:
    questions:
      - q1: do_i_understand_what_was_decided
      - q2: do_i_understand_why
      - q3: would_i_be_tempted_to_reverse_this
    fail_actions:
      q1_no: rewrite_outcome
      q2_no: rewrite_rationale
      q3_yes: expand_rationale_with_alternative_rejection_reasoning

anti_drift:
  - rule: never_skip_session_lifecycle
    enforcement: absolute
  - rule: never_begin_work_before_ingest_audit_init_complete
    enforcement: absolute
  - rule: never_end_session_without_finalize
    enforcement: absolute
  - rule: never_auto_select_a_bootstrap
    enforcement: absolute
    fallback: dispatch_to_operator_driven_dialog
  - rule: never_carry_forward_completed_decisions
    enforcement: absolute
  - rule: finalized_bootstrap_is_current_session_plus_active_carry_forward_only
    enforcement: absolute
  - rule: active_command_docs_must_not_depend_on_session_local_T_or_D_ids_as_durable_authority
    enforcement: absolute
  - rule: verify_live_docs_before_operator_escalation
    enforcement: absolute
  - rule: never_reconstruct_from_memory_when_bootstrap_missing
    fallback: dispatch_to_recovery_protocol_OR_declare_session_zero_with_operator_input
  - rule: never_guess_ambiguous_task_status
    fallback: default_ACTIVE_with_clarification_note
  - rule: bootstrap_wins_over_agent_memory
    enforcement: absolute
  - rule: never_skip_when_user_requests_acceleration
    response: explain_protocol_governance_and_offer_to_speed_up

error_policy:
  MISSING_BOOTSTRAP:
    actions:
      - alert_user
      - dispatch_to_recovery_protocol
      - if_no_valid_recovery_candidate_ask_operator_before_session_zero_per_Q6
    forbidden: reconstruct_from_memory
  BROKEN_BOOTSTRAP:
    definition: parse_failure_OR_schema_failure_OR_data_integrity_failure
    actions:
      - dispatch_to_recovery_protocol_scenario_2_1
    forbidden: silent_skip_or_attempt_to_fix_broken_file_in_place
  STALE_LOCK_PRESENT:
    actions:
      - dispatch_to_recovery_protocol_scenario_2_2
    forbidden: auto_remove_lock
  AMBIGUOUS_TASK_STATUS:
    default: ACTIVE
    required_note: "status unclear — carried as ACTIVE pending clarification"
  CONFLICTING_INFORMATION:
    actions:
      - flag_in_issues_section
      - present_both_versions_to_user
      - request_canonical_answer
    forbidden: silent_resolution
  MISSING_REQUIRED_FIELD:
    fallback_value: "UNKNOWN — {reason}"
    forbidden: [blank, invented_value]
  BOOTSTRAP_DIRECTORY_MISSING:
    action: create_live_directory_only_while_archive_housekeeping_deferred
    log: first_session_bootstrap_for_project

schema_reference:
  template: schema.yaml
  worked_example: example-bootstrap.yaml

schema_fields:
  project:
    name: {type: string, rule: must_match_filename_convention}
    summary: {type: string, length: 2-5_sentences, audience: zero_context_agent, required_content: [what_project_is, current_phase, immediate_trajectory]}
    scope: {type: string, content: project_boundaries}
    non_scope: {type: string, content: explicit_exclusions}
  session:
    id: {type: string, format: YYMMDD-HHMM, must_match: filename_timestamp}
    started: {type: string, format: ISO_8601}
    ended: {type: string, format: ISO_8601, populated_at: finalize_only}
    session_summary: {type: string, length: 2-4_sentences, populated_at: finalize_only, required_content: [what_accomplished, what_remains, open_questions_or_risks]}
  supplemental: {type: boolean, optional: true, populated_when: bootstrap_generated_by_recovery_flow}
  supersedes: {type: string, optional: true, populated_when: supplemental_is_true, content: broken_session_id_being_replaced}
  tasks:
    type: list
    fields:
      id: {type: string, format: T-NNN, permanence: within_session_only}
      title: {type: string, form: imperative_verb_phrase}
      status: {type: enum, values: [ACTIVE, BLOCKED, DEFERRED, DONE, CANCELLED]}
      session_origin: {type: string, content: session_id_where_first_created}
      session_completed: {type: string_or_null, content: session_id_where_DONE_or_CANCELLED}
      priority: {type: enum, values: [HIGH, MEDIUM, LOW], optional: true, recommended_for: ACTIVE}
      description: {type: string, sufficiency: zero_context_agent_can_execute_without_clarification}
      blockers: {type: string_or_null, required_when: status==BLOCKED}
      deferred_reason: {type: string_or_null, required_when: status==DEFERRED, must_include: reactivation_conditions}
      cancelled_reason: {type: string_or_null, required_when: status==CANCELLED}
      notes: {type: string_or_null, optional: true}
  decisions:
    type: list
    permanence: session_scoped
    carry_forward: false
    fields:
      id: {type: string, format: D-NNN, permanence: within_session_only}
      session_origin: {type: string}
      domain: {type: string, examples: [database, UI, architecture, naming]}
      outcome: {type: string, content: concrete_result}
      rationale: {type: string, gate: must_pass_zero_context_test}
      supersedes: {type: string_or_null, content: id_of_replaced_decision_in_same_session_or_named_corpus_artifact}
  environment:
    type: object
    refresh_cadence: every_finalize
    fields:
      tools: {type: list_of_strings}
      key_paths: {type: list_of_strings, scope: ongoing_work_only}
      schema_state: {type: string_or_null, optional: true}
      dependencies: {type: string_or_null, optional: true}
      notes: {type: string_or_null, optional: true}
  context_file_audit:
    type: list
    populated_at: finalize
    consumed_by: next_session_bootstrap-audit_as_pre_check_hint
    fields:
      filename: {type: string, format: relative_to_workspace_root_or_absolute}
      status: {type: enum, values: [CURRENT, STALE, NEEDS_UPDATE, DUPLICATE]}
      note: {type: string_or_null, required_when: status!=CURRENT}
  next_session_kickoff:
    type: object
    populated_at: finalize_only
    consumed_by: next_session_Path_1_handoff_via_bootstrap-ingest_output_and_operator_paste
    carry_forward_into_next_in_memory_bootstrap: false
    fields:
      bootstrap_file_absolute: {type: string, content: absolute_path_of_this_yaml_when_written}
      project_root: {type: string}
      project_name: {type: string}
      path_1_operator_template: {type: string, content: paste_ready_at_reference_plus_execute_intent}
      frozen_intent: {type: list_of_strings, min_items: 1}
      truth_anchors:
        type: object
        fields:
          command_md: {type: string}
          schema_yaml: {type: string}
          validate_script: {type: string, optional_empty: true}
          extra: {type: list_of_strings}
      read_first: {type: list_of_strings, min_items: 2}
      assumptions_next_session_must_hold: {type: list_of_strings}
      known_gaps: {type: list_of_strings}
      do_not_request_from_operator_unless: {type: list_of_strings}
  issues:
    type: list
    optional_section: true
    fields:
      id: {type: string, format: I-NNN}
      summary: {type: string}
      severity: {type: enum, values: [HIGH, MEDIUM, LOW]}
      session_origin: {type: string}
      resolution: {type: string_or_null}
```

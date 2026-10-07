class UnifiedIRValidator:
    """Validate the structural correctness of unified LTH IR."""

    KNOWN_OPCODES = {
        "DEFINE",
        "RULE_BEGIN",
        "CHECK_MEMBER",
        "IF_TRUE",
        "EFFECT",
        "RULE_END",
        "BASE_BEGIN",
        "BASE_OPTION",
        "BASE_END",
        "EXTEND_BASE",
        "EXTENSION_OPTION",
        "FLOW_BEGIN",
        "FLOW_STEP",
        "FLOW_END",
        "SYSTEM_BEGIN",
        "SYSTEM_COMPONENT",
        "SYSTEM_END",
    }

    def validate(self, ir):
        errors = []

        current_rule = None
        current_base = None
        current_extension = None
        current_flow = None
        current_system = None

        seen_definitions = set()
        seen_rules = set()
        seen_bases = set()
        seen_extensions = set()
        seen_flows = set()
        seen_systems = set()

        for index, instruction in enumerate(ir.instructions):
            opcode = instruction.opcode
            operands = instruction.operands

            if opcode not in self.KNOWN_OPCODES:
                errors.append(
                    f"{index}: unknown opcode '{opcode}'"
                )
                continue

            # -------------------------
            # DEFINE
            # -------------------------
            if opcode == "DEFINE":
                if len(operands) != 3:
                    errors.append(
                        f"{index}: DEFINE requires name, kind, value"
                    )
                    continue

                name = operands[0]

                if name in seen_definitions:
                    errors.append(
                        f"{index}: duplicate definition '{name}'"
                    )

                seen_definitions.add(name)

                if any(
                    state is not None
                    for state in (
                        current_rule,
                        current_base,
                        current_flow,
                        current_system,
                    )
                ):
                    errors.append(
                        f"{index}: DEFINE cannot appear inside another block"
                    )

            # -------------------------
            # RULE
            # -------------------------
            elif opcode == "RULE_BEGIN":
                if len(operands) != 1:
                    errors.append(
                        f"{index}: RULE_BEGIN requires rule name"
                    )
                    continue

                if current_rule is not None:
                    errors.append(
                        f"{index}: nested RULE_BEGIN"
                    )

                if any(
                    state is not None
                    for state in (
                        current_base,
                        current_extension,
                        current_flow,
                        current_system,
                    )
                ):
                    errors.append(
                        f"{index}: RULE_BEGIN inside another block"
                    )

                name = operands[0]

                if name in seen_rules:
                    errors.append(
                        f"{index}: duplicate rule '{name}'"
                    )

                seen_rules.add(name)
                current_rule = {
                    "name": name,
                    "condition": False,
                    "effect": False,
                }

            elif opcode == "CHECK_MEMBER":
                if current_rule is None:
                    errors.append(
                        f"{index}: CHECK_MEMBER outside rule"
                    )
                elif len(operands) != 2:
                    errors.append(
                        f"{index}: CHECK_MEMBER requires object and member"
                    )
                else:
                    current_rule["condition"] = True

            elif opcode == "IF_TRUE":
                if current_rule is None:
                    errors.append(
                        f"{index}: IF_TRUE outside rule"
                    )

            elif opcode == "EFFECT":
                if current_rule is None:
                    errors.append(
                        f"{index}: EFFECT outside rule"
                    )
                elif len(operands) != 3:
                    errors.append(
                        f"{index}: EFFECT requires target, operator, value"
                    )
                else:
                    current_rule["effect"] = True

            elif opcode == "RULE_END":
                if current_rule is None:
                    errors.append(
                        f"{index}: RULE_END without RULE_BEGIN"
                    )
                    continue

                if len(operands) != 1:
                    errors.append(
                        f"{index}: RULE_END requires rule name"
                    )

                if not current_rule["condition"]:
                    errors.append(
                        f"{index}: rule has no condition"
                    )

                if not current_rule["effect"]:
                    errors.append(
                        f"{index}: rule has no effect"
                    )

                if len(operands) == 1 and operands[0] != current_rule["name"]:
                    errors.append(
                        f"{index}: RULE_END name mismatch"
                    )

                current_rule = None

            # -------------------------
            # BASE
            # -------------------------
            elif opcode == "BASE_BEGIN":
                if len(operands) != 2:
                    errors.append(
                        f"{index}: BASE_BEGIN requires name and service"
                    )
                    continue

                if any(
                    state is not None
                    for state in (
                        current_rule,
                        current_base,
                        current_flow,
                        current_system,
                    )
                ):
                    errors.append(
                        f"{index}: BASE_BEGIN inside another block"
                    )

                name = operands[0]

                if name in seen_bases:
                    errors.append(
                        f"{index}: duplicate base '{name}'"
                    )

                seen_bases.add(name)
                current_base = name

            elif opcode == "BASE_OPTION":
                if current_base is None:
                    errors.append(
                        f"{index}: BASE_OPTION outside base"
                    )
                elif len(operands) != 3:
                    errors.append(
                        f"{index}: BASE_OPTION requires base, name, value"
                    )
                elif operands[0] != current_base:
                    errors.append(
                        f"{index}: BASE_OPTION base mismatch"
                    )

            elif opcode == "BASE_END":
                if current_base is None:
                    errors.append(
                        f"{index}: BASE_END without BASE_BEGIN"
                    )
                elif len(operands) != 1:
                    errors.append(
                        f"{index}: BASE_END requires base name"
                    )
                elif operands[0] != current_base:
                    errors.append(
                        f"{index}: BASE_END name mismatch"
                    )
                else:
                    current_base = None

            # -------------------------
            # BASE EXTENSION
            # -------------------------
            elif opcode == "EXTEND_BASE":
                if len(operands) != 2:
                    errors.append(
                        f"{index}: EXTEND_BASE requires extension and base"
                    )
                    continue

                if any(
                    state is not None
                    for state in (
                        current_rule,
                        current_base,
                        current_flow,
                        current_system,
                    )
                ):
                    errors.append(
                        f"{index}: EXTEND_BASE inside another block"
                    )

                name = operands[0]

                if name in seen_extensions:
                    errors.append(
                        f"{index}: duplicate base extension '{name}'"
                    )

                seen_extensions.add(name)
                current_extension = name

            elif opcode == "EXTENSION_OPTION":
                if current_extension is None:
                    errors.append(
                        f"{index}: EXTENSION_OPTION outside extension"
                    )
                elif len(operands) != 3:
                    errors.append(
                        f"{index}: EXTENSION_OPTION requires extension, name, value"
                    )
                elif operands[0] != current_extension:
                    errors.append(
                        f"{index}: EXTENSION_OPTION extension mismatch"
                    )

            # -------------------------
            # FLOW
            # -------------------------
            elif opcode == "FLOW_BEGIN":
                if len(operands) != 1:
                    errors.append(
                        f"{index}: FLOW_BEGIN requires flow name"
                    )
                    continue

                if any(
                    state is not None
                    for state in (
                        current_rule,
                        current_base,
                        current_flow,
                        current_system,
                    )
                ):
                    errors.append(
                        f"{index}: FLOW_BEGIN inside another block"
                    )

                name = operands[0]

                if name in seen_flows:
                    errors.append(
                        f"{index}: duplicate flow '{name}'"
                    )

                seen_flows.add(name)
                current_flow = name

            elif opcode == "FLOW_STEP":
                if current_flow is None:
                    errors.append(
                        f"{index}: FLOW_STEP outside flow"
                    )
                elif len(operands) != 2:
                    errors.append(
                        f"{index}: FLOW_STEP requires flow and step"
                    )
                elif operands[0] != current_flow:
                    errors.append(
                        f"{index}: FLOW_STEP flow mismatch"
                    )

            elif opcode == "FLOW_END":
                if current_flow is None:
                    errors.append(
                        f"{index}: FLOW_END without FLOW_BEGIN"
                    )
                elif len(operands) != 1:
                    errors.append(
                        f"{index}: FLOW_END requires flow name"
                    )
                elif operands[0] != current_flow:
                    errors.append(
                        f"{index}: FLOW_END name mismatch"
                    )
                else:
                    current_flow = None

            # -------------------------
            # SYSTEM
            # -------------------------
            elif opcode == "SYSTEM_BEGIN":
                if len(operands) != 1:
                    errors.append(
                        f"{index}: SYSTEM_BEGIN requires system name"
                    )
                    continue

                if any(
                    state is not None
                    for state in (
                        current_rule,
                        current_base,
                        current_flow,
                        current_system,
                    )
                ):
                    errors.append(
                        f"{index}: SYSTEM_BEGIN inside another block"
                    )

                name = operands[0]

                if name in seen_systems:
                    errors.append(
                        f"{index}: duplicate system '{name}'"
                    )

                seen_systems.add(name)
                current_system = name

            elif opcode == "SYSTEM_COMPONENT":
                if current_system is None:
                    errors.append(
                        f"{index}: SYSTEM_COMPONENT outside system"
                    )
                elif len(operands) != 3:
                    errors.append(
                        f"{index}: SYSTEM_COMPONENT requires system, index, name"
                    )
                elif operands[0] != current_system:
                    errors.append(
                        f"{index}: SYSTEM_COMPONENT system mismatch"
                    )

            elif opcode == "SYSTEM_END":
                if current_system is None:
                    errors.append(
                        f"{index}: SYSTEM_END without SYSTEM_BEGIN"
                    )
                elif len(operands) != 1:
                    errors.append(
                        f"{index}: SYSTEM_END requires system name"
                    )
                elif operands[0] != current_system:
                    errors.append(
                        f"{index}: SYSTEM_END name mismatch"
                    )
                else:
                    current_system = None

        # -------------------------
        # Unclosed blocks
        # -------------------------
        if current_rule is not None:
            errors.append(
                f"unclosed rule '{current_rule['name']}'"
            )

        if current_base is not None:
            errors.append(
                f"unclosed base '{current_base}'"
            )

        if current_flow is not None:
            errors.append(
                f"unclosed flow '{current_flow}'"
            )

        if current_system is not None:
            errors.append(
                f"unclosed system '{current_system}'"
            )

        return errors

    def is_valid(self, ir):
        return not self.validate(ir)

    def describe(self, ir):
        errors = self.validate(ir)

        if not errors:
            return "UNIFIED IR VALID"

        lines = ["UNIFIED IR INVALID"]

        for error in errors:
            lines.append(f"  {error}")

        return "\n".join(lines)

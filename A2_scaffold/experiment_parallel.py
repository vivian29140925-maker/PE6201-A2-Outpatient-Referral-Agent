"""
D2(c) experiment
Sequential versus parallel independent tool calls.

Same case.
Same tools.
Same routing outcome.
Only grouping of independent calls changes.
"""

import copy

import agent
import backends


CASE_ID = "REF-5602"


# -------------------------------------------------------
# Sequential version
# -------------------------------------------------------

SEQUENTIAL_SCRIPT = [
    {
        "thought": "Fetch the referral.",
        "calls": [
            (
                "get_referral",
                {"referral_id": CASE_ID},
            )
        ],
    },

    {
        "thought": "Check referral criteria.",
        "calls": [
            (
                "check_referral_criteria",
                {
                    "specialty": "OPH",
                    "referral_id": CASE_ID,
                },
            )
        ],
    },

    {
        "thought": "Now inspect patient history.",
        "calls": [
            (
                "lookup_patient",
                {"patient_id": "P-1180"},
            )
        ],
    },

    {
        "thought":
            "Search the first half of the valid routine window.",
        "calls": [
            (
                "get_clinic_slots",
                {
                    "specialty": "OPH",
                    "band": "routine",
                    "from": "2026-09-09",
                    "to": "2026-09-30",
                },
            )
        ],
    },

    {
        "thought":
            "No available routine slot was found in the first half. "
            "Search the second half.",
        "calls": [
            (
                "get_clinic_slots",
                {
                    "specialty": "OPH",
                    "band": "routine",
                    "from": "2026-10-01",
                    "to": "2026-11-04",
                },
            )
        ],
    },

    {
        "thought":
            "Book the first valid available routine slot.",
        "calls": [
            (
                "book_slot",
                {
                    "clinic": "OPH-C2",
                    "date": "2026-10-14",
                    "time": "11:20",
                    "referral_id": CASE_ID,
                },
            )
        ],
    },

    {
        "final": {
            "decision": "book",
            "booked": {
                "clinic": "OPH-C2",
                "date": "2026-10-14",
                "time": "11:20",
            },
            "reason":
                "Routine Ophthalmology referral. VF-01 present, "
                "no existing OPH appointment, and the first available "
                "routine slot inside the eight-week window was "
                "2026-10-14 11:20.",
        },
        "thought": "Finish.",
    },
]


# -------------------------------------------------------
# Existing scaffold = parallel version
# -------------------------------------------------------

PARALLEL_SCRIPT = copy.deepcopy(
    backends.SCRIPTS[CASE_ID]
)


def run_with_script(script):
    original = backends.SCRIPTS[CASE_ID]

    try:
        backends.SCRIPTS[CASE_ID] = script

        result = agent.run_case(
            CASE_ID,
            problem="B",
            verbose=False,
        )

        return result

    finally:
        backends.SCRIPTS[CASE_ID] = original


def print_result(label, result):
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)

    print("decision:     ", result.get("decision"))
    print("turns:        ", result.get("turns"))
    print("tokens_in:    ", result.get("tokens_in"))
    print("tokens_out:   ", result.get("tokens_out"))
    print("cost_usd:     ", result.get("cost_usd"))
    print("tool calls:   ", len(result.get("evidence", [])))
    print("evidence:     ", result.get("evidence"))


if __name__ == "__main__":

    sequential = run_with_script(
        SEQUENTIAL_SCRIPT
    )

    parallel = run_with_script(
        PARALLEL_SCRIPT
    )

    print_result(
        "SEQUENTIAL",
        sequential,
    )

    print_result(
        "PARALLEL",
        parallel,
    )

    print("\n" + "=" * 60)
    print("IMPROVEMENT")
    print("=" * 60)

    turns_saved = (
        sequential["turns"]
        - parallel["turns"]
    )

    token_saving = (
        sequential["tokens_in"]
        - parallel["tokens_in"]
    )

    token_pct = (
        token_saving
        / sequential["tokens_in"]
        * 100
        if sequential["tokens_in"]
        else 0
    )

    print(
        f"Turns saved: {turns_saved}"
    )

    print(
        f"Estimated input tokens saved: "
        f"{token_saving}"
    )

    print(
        f"Estimated input-token reduction: "
        f"{token_pct:.1f}%"
    )

    print(
        "Same decision:",
        sequential["decision"]
        == parallel["decision"],
    )
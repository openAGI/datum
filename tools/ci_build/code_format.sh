#!/usr/bin/env bash
# ==============================================================================
#
# Usage: code_format.sh [--incremental] [--in-place]
#
# Options:
#  --incremental  Performs checks incrementally, by using the files changed in
#                 the latest commit
#  --in-place  make changes to files in place

# Current script directory
SCRIPT_DIR=$( cd ${0%/*} && pwd -P )
source "${SCRIPT_DIR}/builds/builds_common.sh"

ROOT_DIR=$( cd "$SCRIPT_DIR/../.." && pwd -P )
if [[ ! -d "datum" ]]; then
    echo "ERROR: PWD: $PWD is not project root"
    exit 1
fi

# Parse command-line arguments
INCREMENTAL_FLAG=""
IN_PLACE_FLAG=""
UNRESOLVED_ARGS=""

for arg in "$@"; do
    if [[ "${arg}" == "--incremental" ]]; then
        INCREMENTAL_FLAG="--incremental"
    elif [[ "${arg}" == "--in-place" ]]; then
        IN_PLACE_FLAG="--in-place"
    else
        UNRESOLVED_ARGS="${UNRESOLVED_ARGS} ${arg}"
    fi
done

if [[ ! -z "$UNRESOLVED_ARGS" ]]; then
    die "ERROR: Found unsupported args: $UNRESOLVED_ARGS"
fi

do_python_format_check() {
    PYTHON_SRC_FILES=$(get_py_files_to_check $INCREMENTAL_FLAG)
    if [[ -z $PYTHON_SRC_FILES ]]; then
        echo "do_python_format_check will NOT run due to"\
             "the absence of code changes."
        return 0
    fi

    NUM_BUILD_FILES=$(echo ${PYTHON_SRC_FILES} | wc -w)
    echo "Running do_python_format_check on ${NUM_BUILD_FILES} files"
    echo ""

    YAPFRC_FILE="${SCRIPT_DIR}/yapfrc"
    if [[ ! -f "${YAPFRC_FILE}" ]]; then
        die "ERROR: Cannot find yapf rc file at ${YAPFRC_FILE}"
    fi
    YAPF_OPTS="--style=$YAPFRC_FILE --parallel"

    if [[ ! -z $IN_PLACE_FLAG ]]; then
        echo "Auto format..."
				isort $PYTHON_SRC_FILES
        yapf $YAPF_OPTS --in-place --verbose $PYTHON_SRC_FILES
        docformatter --wrap-summaries 101 --wrap-descriptions 99 --in-place $PYTHON_SRC_FILES
    fi

		FAIL_COUNTER=0

    UNFORMATTED_CODES=$(yapf $YAPF_OPTS --diff $PYTHON_SRC_FILES)
    if [[ $? != "0" || ! -z "$UNFORMATTED_CODES" ]]; then
        echo "Find unformatted codes:"
        echo "$UNFORMATTED_CODES"
        echo "Python yapf format check fails."
				((FAIL_COUNTER++))
    else
        echo "Python yapf format check success."
    fi
		return ${FAIL_COUNTER}
}

# Supply all auto format step commands and descriptions
FORMAT_STEPS=("do_python_format_check")
FORMAT_STEPS_DESC=("Check python file format")

FAIL_COUNTER=0
PASS_COUNTER=0
STEP_EXIT_CODES=()

# Execute all the auto format steps
COUNTER=0
while [[ ${COUNTER} -lt "${#FORMAT_STEPS[@]}" ]]; do
    INDEX=COUNTER
    ((INDEX++))

    echo ""
    echo "--- Format check step ${INDEX} of ${#FORMAT_STEPS[@]}: "\
         "${FORMAT_STEPS[COUNTER]} (${FORMAT_STEPS_DESC[COUNTER]}) ---"
    echo ""

    # subshell: don't leak variables or changes of working directory
    (
    ${FORMAT_STEPS[COUNTER]}
    )
    RESULT=$?

    if [[ ${RESULT} != "0" ]]; then
        ((FAIL_COUNTER++))
    else
        ((PASS_COUNTER++))
    fi

    STEP_EXIT_CODES+=(${RESULT})

    echo ""
    ((COUNTER++))
done

# Print summary of results
COUNTER=0
echo "---- Summary of format check results ----"
while [[ ${COUNTER} -lt "${#FORMAT_STEPS[@]}" ]]; do
    INDEX=COUNTER
    ((INDEX++))

    echo "${INDEX}. ${FORMAT_STEPS[COUNTER]}: ${FORMAT_STEPS_DESC[COUNTER]}"
    if [[ ${STEP_EXIT_CODES[COUNTER]} == "0" ]]; then
        printf "  ${COLOR_GREEN}PASS${COLOR_NC}\n"
    else
        printf "  ${COLOR_RED}FAIL${COLOR_NC}\n"
    fi

    ((COUNTER++))
done

echo
echo "${FAIL_COUNTER} failed; ${PASS_COUNTER} passed."

echo
if [[ ${FAIL_COUNTER} == "0" ]]; then
    printf "Format checks ${COLOR_GREEN}PASSED${COLOR_NC}\n"
else
    printf "Use ${COLOR_GREEN}make code-format${COLOR_NC} command to format codes automatically\n"
    printf "Format checks ${COLOR_RED}FAILED${COLOR_NC}\n"
    exit 1
fi

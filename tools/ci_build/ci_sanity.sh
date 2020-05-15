#!/usr/bin/env bash
# ==============================================================================
#
# Usage: ci_sanity.sh [--pycodestyle] [--incremental]
#
# Options:
#           run sanity checks: python 3 pylint checks
#  --pycodestyle   run pycodestyle test only
#  --incremental  Performs checks incrementally, by using the files changed in
#                 the latest commit

# Current script directory
SCRIPT_DIR=$( cd ${0%/*} && pwd -P )
source "${SCRIPT_DIR}/builds/builds_common.sh"

ROOT_DIR=$( cd "$SCRIPT_DIR/../.." && pwd -P )
if [[ ! -d "datum" ]]; then
    echo "ERROR: PWD: $PWD is not project root"
    exit 1
fi

# Run pylint
do_pylint() {
    # Usage: do_pylint [--incremental]
    #
    # Options:
    #   --incremental  Performs check on only the python files changed in the
    #                  last non-merge git commit.

    # Use this list to whitelist pylint errors
    ERROR_WHITELIST=""

    echo "ERROR_WHITELIST=\"${ERROR_WHITELIST}\""

    PYLINT_BIN="python3 -m pylint"

    PYTHON_SRC_FILES=$(get_py_files_to_check $1)
    if [[ -z ${PYTHON_SRC_FILES} ]]; then
        echo "do_pylint found no Python files to check. Returning."
        return 0
    fi

    PYLINTRC_FILE="${SCRIPT_DIR}/pylintrc"

    if [[ ! -f "${PYLINTRC_FILE}" ]]; then
        die "ERROR: Cannot find pylint rc file at ${PYLINTRC_FILE}"
    fi

    NUM_SRC_FILES=$(echo ${PYTHON_SRC_FILES} | wc -w)
    NUM_CPUS=$(num_cpus)

    echo "Running pylint on ${NUM_SRC_FILES} files with ${NUM_CPUS} "\
    "parallel jobs..."
    echo ""

    PYLINT_START_TIME=$(date +'%s')
    OUTPUT_FILE="$(mktemp)_pylint_output.log"
    ERRORS_FILE="$(mktemp)_pylint_errors.log"
    NONWL_ERRORS_FILE="$(mktemp)_pylint_nonwl_errors.log"

    rm -rf ${OUTPUT_FILE}
    rm -rf ${ERRORS_FILE}
    rm -rf ${NONWL_ERRORS_FILE}
    touch ${NONWL_ERRORS_FILE}

    ${PYLINT_BIN} --rcfile="${PYLINTRC_FILE}" --output-format=parseable \
        --jobs=4 ${PYTHON_SRC_FILES} > ${OUTPUT_FILE} 2>&1
    PYLINT_END_TIME=$(date +'%s')

    echo ""
    echo "pylint took $((PYLINT_END_TIME - PYLINT_START_TIME)) s"
    echo ""
		echo ${OUTPUT_FILE}

    # Report only what we care about
    # Ref https://pylint.readthedocs.io/en/latest/technical_reference/features.html
    # E: all errors
    # W0311 bad-indentation
    # W0312 mixed-indentation
    # C0330 bad-continuation
    # C0301 line-too-long
    # C0326 bad-whitespace
    # W0611 unused-import
    # W0622 redefined-builtin
    grep -E '(\[E|\[W0311|\[W0312|\[C0330|\[C0301|\[C0326|\[W0611|\[W0622)' ${OUTPUT_FILE} > ${ERRORS_FILE}

    N_ERRORS=0
    while read -r LINE; do
        IS_WHITELISTED=0
        for WL_REGEX in ${ERROR_WHITELIST}; do
            if echo ${LINE} | grep -q "${WL_REGEX}"; then
                echo "Found a whitelisted error:"
                echo "  ${LINE}"
                IS_WHITELISTED=1
            fi
        done

        if [[ ${IS_WHITELISTED} == "0" ]]; then
            echo "${LINE}" >> ${NONWL_ERRORS_FILE}
            echo "" >> ${NONWL_ERRORS_FILE}
            ((N_ERRORS++))
        fi
    done <${ERRORS_FILE}

    echo ""
    if [[ ${N_ERRORS} != 0 ]]; then
        echo "FAIL: Found ${N_ERRORS} non-whitelited pylint errors:"
        cat "${NONWL_ERRORS_FILE}"
        return 1
    else
        echo "PASS: No non-whitelisted pylint errors were found."
        return 0
    fi
}

# Run pycodestyle check
do_pycodestyle() {
    # Usage: do_pycodestyle [--incremental]
    # Options:
    #   --incremental  Performs check on only the python files changed in the
    #                  last non-merge git commit.

    pycodestyle_CONFIG_FILE="${SCRIPT_DIR}/pycodestyle"

    if [[ "$1" == "--incremental" ]]; then
        PYTHON_SRC_FILES=$(get_py_files_to_check --incremental)
        NUM_PYTHON_SRC_FILES=$(echo ${PYTHON_SRC_FILES} | wc -w)

        echo "do_pycodestyle will perform checks on only the ${NUM_PYTHON_SRC_FILES} "\
             "Python file(s) changed in the last non-merge git commit due to the "\
             "--incremental flag:"
        echo "${PYTHON_SRC_FILES}"
        echo ""
    else
        PYTHON_SRC_FILES=$(get_py_files_to_check)
    fi

    if [[ -z ${PYTHON_SRC_FILES} ]]; then
        echo "do_pycodestyle found no Python files to check. Returning."
        return 0
    fi

    if [[ ! -f "${pycodestyle_CONFIG_FILE}" ]]; then
        die "ERROR: Cannot find pycodestyle config file at ${pycodestyle_CONFIG_FILE}"
    fi
    echo "See \"${pycodestyle_CONFIG_FILE}\" for pycodestyle config( e.g., ignored errors)"

    NUM_SRC_FILES=$(echo ${PYTHON_SRC_FILES} | wc -w)

    echo "Running pycodestyle on ${NUM_SRC_FILES} files"
    echo ""

    pycodestyle_START_TIME=$(date +'%s')
    pycodestyle_OUTPUT_FILE="$(mktemp)_pycodestyle_output.log"

    rm -rf ${pycodestyle_OUTPUT_FILE}

    pycodestyle --config="${pycodestyle_CONFIG_FILE}" --statistics \
        ${PYTHON_SRC_FILES} 2>&1 | tee ${pycodestyle_OUTPUT_FILE}
    pycodestyle_END_TIME=$(date +'%s')

    echo ""
    echo "pycodestyle took $((pycodestyle_END_TIME - pycodestyle_START_TIME)) s"
    echo ""

    if [[ -s ${pycodestyle_OUTPUT_FILE} ]]; then
        echo "FAIL: pycodestyle found above errors and/or warnings."
        return 1
    else
        echo "PASS: No pycodestyle errors or warnings were found"
        return 0
    fi
}

do_check_file_name_test() {
    cd "$ROOT_DIR/tools/ci_build/verify"
    python check_file_name.py
}

do_check_code_format_test() {
    CHECK_CMD="$SCRIPT_DIR/code_format.sh $1"
    ${CHECK_CMD}
}

# Supply all sanity step commands and descriptions
SANITY_STEPS=("do_check_code_format_test" "do_pylint" "do_pycodestyle" "do_check_file_name_test")
SANITY_STEPS_DESC=("Check code style" "Python 3 pylint" " pycodestyle test" "Check file names for cases")

INCREMENTAL_FLAG=""

for arg in "$@"; do
    if [[ "${arg}" == "--incremental" ]]; then
        INCREMENTAL_FLAG="--incremental"
    fi
done


FAIL_COUNTER=0
PASS_COUNTER=0
STEP_EXIT_CODES=()

# Execute all the sanity build steps
COUNTER=0
while [[ ${COUNTER} -lt "${#SANITY_STEPS[@]}" ]]; do
    INDEX=COUNTER
    ((INDEX++))

    echo ""
    echo "=== Sanity check step ${INDEX} of ${#SANITY_STEPS[@]}: "\
         "${SANITY_STEPS[COUNTER]} (${SANITY_STEPS_DESC[COUNTER]}) ==="
    echo ""

    # subshell: don't leak variables or changes of working directory
    (
    ${SANITY_STEPS[COUNTER]} ${INCREMENTAL_FLAG}
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

# Print summary of build results
COUNTER=0
echo "==== Summary of sanity check results ===="
while [[ ${COUNTER} -lt "${#SANITY_STEPS[@]}" ]]; do
    INDEX=COUNTER
    ((INDEX++))

    echo "${INDEX}. ${SANITY_STEPS[COUNTER]}: ${SANITY_STEPS_DESC[COUNTER]}"
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
    printf "Sanity checks ${COLOR_GREEN}PASSED${COLOR_NC}\n"
else
    printf "Sanity checks ${COLOR_RED}FAILED${COLOR_NC}\n"
    exit 1
fi

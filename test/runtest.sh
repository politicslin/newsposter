PROJECT_WORKSPACE="$HOME/workspace-gae/newsposter"
export PYTHONPATH="$HOME/bin/google_appengine:$PYTHONPATH"
export PYTHONPATH="$PROJECT_WORKSPACE/src:$PROJECT_WORKSPACE/src/library:$PYTHONPATH"
export PYTHONPATH="$PROJECT_WORKSPACE/src:$PYTHONPATH"
python "$PROJECT_WORKSPACE/test/unit/testcontentposter/testcpapi.py"


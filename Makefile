streamlit_cloud:
	-@API_URL=cloud_api_uri streamlit run HandSpell.py

streamlit_local:
	streamlit run HandSpell.py --server.runOnSave true

# This refactors the code by black's standards
black:
	uv run black -l 100 HandSpell.py style.py utils.py pages/

# This check the differences proposed by black
black_diff:
	uv run black -l 100 --diff HandSpell.py style.py utils.py pages/

# Runs pylint check if code is according to standards
pylint:
	uv run pylint HandSpell.py style.py utils.py pages/

# Checks code
# check_code:
# make black pylint

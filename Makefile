streamlit_cloud:
	-@API_URL=cloud_api_uri streamlit run HandSpell.py

streamlit_local:
	streamlit run HandSpell.py --server.runOnSave true

black:
	uv run black .

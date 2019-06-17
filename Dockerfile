FROM beyselein/py_correction_base_image

COPY main.py main_helpers.py test_data.schema.json /data/

ENTRYPOINT ["python3", "main.py"]
FROM ls6uniwue/py_correction_base_image

COPY model.py main.py main_helpers.py test_data.schema.json /data/

ENTRYPOINT ["python", "main.py"]

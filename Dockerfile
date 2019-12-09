FROM beyselein/py_correction_base_image

RUN pip install typing_extensions

COPY main.py main_helpers.py test_data.schema.json /data/

ENTRYPOINT ["python", "main.py"]
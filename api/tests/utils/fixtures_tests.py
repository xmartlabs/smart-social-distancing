import pytest
import shutil
import os
import copy
from pathlib import Path

from fastapi.testclient import TestClient

from libs.config_engine import ConfigEngine
from api.settings import Settings
from api.tests.utils.common_functions import create_app_config

from .example_models import camera_template, camera_example, camera_example_2, camera_example_3, camera_example_4,\
    area_example, area_example_2


def config_rollback_base(option="MAIN"):
    original_path = ""
    if option == "EMPTY":
        """
        Empty template with no camera or area.
        """
        original_path = "/repo/api/tests/data/config-x86-openvino_EMPTY.ini"
    elif option == "MAIN":
        """
        Here there are charged only 2 cameras:
            camera_example (ID: 49)
            camera_example_2 (ID: 50)
        """
        original_path = "/repo/api/tests/data/config-x86-openvino_MAIN.ini"
    elif option == "METRICS":
        """
        Here there are charged 4 cameras and two areas:
            camera_example (ID: 49), Area 5
            camera_example_2 (ID: 50), Area 5
            camera_example_3 (ID: 51), Area 6
            camera_example_4 (ID: 52), Area 6
        """
        original_path = "/repo/api/tests/data/config-x86-openvino_METRICS.ini"
    config_sample_path_to_modify = "/repo/api/tests/data/config-x86-openvino_TEMPORARY.ini"
    shutil.copyfile(original_path, config_sample_path_to_modify)

    config = ConfigEngine(config_sample_path_to_modify)
    Settings(config=config)

    # Import ProcessorAPI after Settings has been initialized with a config.
    from api.processor_api import ProcessorAPI

    app_instance = ProcessorAPI()
    api = app_instance.app
    client = TestClient(api)
    return client, config_sample_path_to_modify


@pytest.fixture
def rollback_camera_template():
    yield None
    for i in [str(camera_template["id"]), str(int(camera_template["id"]) + 1)]:
        camera_screenshot_directory = os.path.join(os.environ.get("ScreenshotsDirectory"), i)
        if os.path.exists(camera_screenshot_directory):
            shutil.rmtree(camera_screenshot_directory)
        camera_directory = os.path.join(os.environ.get("SourceLogDirectory"), i)
        if os.path.exists(camera_directory):
            shutil.rmtree(camera_directory)


@pytest.fixture
def config_rollback():
    client, config_sample_path_to_modify = config_rollback_base(option="EMPTY")
    yield client, config_sample_path_to_modify
    os.remove(config_sample_path_to_modify)

"""
def create_camera(client, example_camera):
    camera_sample = copy.deepcopy(example_camera)
    return client.post("/cameras", json=camera_sample)


def delete_camera(client, camera_id):
    client.delete(f'/cameras/{camera_id}')


def config_rollback_create_cameras_base():
    client, config_sample_path_to_modify = config_rollback_base()

    response_camera_1 = create_camera(client, copy.deepcopy(camera_example))
    response_camera_2 = create_camera(client, copy.deepcopy(camera_example_2))

    return response_camera_1.json(), response_camera_2.json(), client, config_sample_path_to_modify


@pytest.fixture
def config_rollback_create_cameras():
    camera, camera_2, client, config_sample_path = config_rollback_create_cameras_base()

    yield camera, camera_2, client, config_sample_path

    # Delete cameras
    delete_camera(client, camera_example['id'])
    delete_camera(client, camera_example_2['id'])

    # We have to remove .ini file after every endpoint call
    os.remove(config_sample_path)
"""

"""
def create_area(client, example_area):
    area_sample = copy.deepcopy(example_area)
    return client.post("/areas", json=area_sample)


def delete_area(client, camera_id):
    client.delete(f'/areas/{camera_id}')
"""

@pytest.fixture
def config_rollback_areas():
    client, config_sample_path_to_modify = config_rollback_base(option="METRICS")
    yield area_example, area_example_2, client, config_sample_path_to_modify
    os.remove(config_sample_path_to_modify)


@pytest.fixture
def config_rollback_cameras():
    client, config_sample_path_to_modify = config_rollback_base()
    yield camera_example, camera_example_2, client, config_sample_path_to_modify
    os.remove(config_sample_path_to_modify)

"""
@pytest.fixture
def config_rollback_create_areas():
    "" First we have to create cameras ""
    client, config_sample_path_to_modify = config_rollback_base()

    # Create several cameras
    create_camera(client, copy.deepcopy(camera_example))
    create_camera(client, copy.deepcopy(camera_example_2))
    create_camera(client, copy.deepcopy(camera_example_3))
    create_camera(client, copy.deepcopy(camera_example_4))

    # Create areas
    response_area_1 = create_area(client, area_example)
    response_area_2 = create_area(client, area_example_2)

    yield response_area_1.json(), response_area_2.json(), client, config_sample_path_to_modify
    ""
    # Delete areas
    delete_area(client, area_example['id'])
    delete_area(client, area_example_2['id'])

    # Delete cameras
    delete_camera(client, camera_example['id'])
    delete_camera(client, camera_example_2['id'])
    delete_camera(client, camera_example_3['id'])
    delete_camera(client, camera_example_4['id'])
    ""
    # We have to remove .ini file after every endpoint call
    os.remove(config_sample_path_to_modify)
"""


@pytest.fixture
def app_config():
    app_config = create_app_config()
    return app_config


@pytest.fixture
def camera_sample():
    camera_sample = copy.deepcopy(camera_template)
    return camera_sample

"""
@pytest.fixture
def rollback_screenshot_camera_folder():
    yield None
    # Deletes only the camera screenshots directory and all its content.
    camera_screenshot_directory = os.path.join(os.environ.get("ScreenshotsDirectory"), str(camera_template["id"]))
    if os.path.exists(camera_screenshot_directory):
        shutil.rmtree(camera_screenshot_directory)
"""


@pytest.fixture
def rollback_homography_matrix_folder():
    yield None
    # Deletes the homography_matrix directory and all its content.
    raw = os.environ.get("SourceLogDirectory")
    path = os.path.join(raw, str(camera_template["id"]))
    if os.path.exists(path):
        shutil.rmtree(path)


@pytest.fixture
def h_inverse_matrix():
    return {"h_inverse.txt": "h_inv: 0.8196721311475405 0.6333830104321896 -302.9061102831591 -1.8201548094104302e-16 "
                             "1.7138599105812207 -531.2965722801783 -2.7856282300542207e-18 0.008047690014903118 "
                             "-1.4947839046199658"}


@pytest.fixture
def pts_destination():
    return {
        "pts_destination": [
            [
                130,
                310
            ],
            [
                45,
                420
            ],
            [
                275,
                420
            ],
            [
                252,
                310
            ]
        ]
    }


@pytest.fixture
def heatmap_simulation():
    os.environ["HeatMapPath"] = "/repo/api/tests/data/mocked_data/data/processor/static/data/sources/"
    # Creates heatmaps directory
    heatmap_directory = os.path.join(os.getenv("SourceLogDirectory"), camera_example['id'], "heatmaps")
    Path(heatmap_directory).mkdir(parents=True, exist_ok=True)
    # Copy file to heatmaps to directory
    original_path_violations = "/repo/api/tests/data/violations_heatmap_2020-09-19_EXAMPLE.npy"
    original_path_detections = "/repo/api/tests/data/detections_heatmap_2020-09-19_EXAMPLE.npy"
    heatmap_path_to_modify_violations = os.path.join(heatmap_directory, "violations_heatmap_2020-09-19.npy")
    heatmap_path_to_modify_detections = os.path.join(heatmap_directory, "detections_heatmap_2020-09-19.npy")
    shutil.copyfile(original_path_violations, heatmap_path_to_modify_violations)
    shutil.copyfile(original_path_detections, heatmap_path_to_modify_detections)
    # Generates more data
    new_heatmap_path_to_modify_violations = os.path.join(heatmap_directory, "violations_heatmap_2020-09-22.npy")
    new_heatmap_path_to_modify_detections = os.path.join(heatmap_directory, "detections_heatmap_2020-09-22.npy")
    shutil.copyfile(original_path_detections, new_heatmap_path_to_modify_violations)
    shutil.copyfile(original_path_violations, new_heatmap_path_to_modify_detections)
    yield None
    # Deletes everything
    shutil.rmtree(heatmap_directory)

"""
def copy_tree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
"""

"""
def create_reports(id_camera, optional=False):
    if optional:
        fromDirectory = "/repo/api/tests/data/reports_EXAMPLE_2/"
    else:
        fromDirectory = "/repo/api/tests/data/reports_EXAMPLE/"
    reports_directory = os.path.join(os.getenv("SourceLogDirectory"), id_camera, "reports")
    copy_tree(fromDirectory, reports_directory)
"""

"""
def delete_reports(id_camera):
    # Deletes everything
    reports_directory = os.path.join(os.getenv("SourceLogDirectory"), id_camera, "reports")
    shutil.rmtree(reports_directory)
"""

"""
def create_report_occupancy(id_camera, optional=False):
    if optional:
        fromDirectory = "/repo/api/tests/data/reports_occupancy_EXAMPLE_2/"
    else:
        fromDirectory = "/repo/api/tests/data/reports_occupancy_EXAMPLE/"
    reports_directory = os.path.join(os.getenv("AreaLogDirectory"), id_camera, "reports")
    copy_tree(fromDirectory, reports_directory)
"""

"""
def delete_report_occupancy(id_camera):
    # Deletes everything
    reports_directory = os.path.join(os.getenv("AreaLogDirectory"), id_camera, "reports")
    shutil.rmtree(reports_directory)
"""

"""
@pytest.fixture
def reports_simulation():
    create_reports(camera_example['id'])
    create_reports(camera_example_2['id'])
    yield None
    delete_reports(camera_example['id'])
    delete_reports(camera_example_2['id'])
"""

"""
@pytest.fixture
def reports_simulation_areas():
    create_reports(camera_example['id'])
    create_reports(camera_example_2['id'], optional=True)
    create_reports(camera_example_3['id'])
    create_reports(camera_example_4['id'])
    create_report_occupancy(area_example['id'])
    create_report_occupancy(area_example_2['id'], optional=True)
    import pdb
    pdb.set_trace()
    yield None
    ""
    delete_reports(camera_example['id'])
    delete_reports(camera_example_2['id'])
    delete_reports(camera_example_3['id'])
    delete_reports(camera_example_4['id'])
    delete_report_occupancy(area_example['id'])
    delete_report_occupancy(area_example_2['id'])
    ""
"""
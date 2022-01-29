from typing import Optional

from flask import current_app

from qcfractal.app import main, storage_socket
from qcfractal.app.helpers import get_helper, prefix_projection
from qcfractal.app.routes import wrap_route
from qcportal.base_models import CommonGetProjURLParameters
from qcportal.exceptions import LimitExceededError
from qcportal.records.torsiondrive import TorsiondriveAddBody, TorsiondriveQueryBody
from qcportal.utils import calculate_limit


@main.route("/v1/record/torsiondrive", methods=["POST"])
@wrap_route(TorsiondriveAddBody, None)
def add_torsiondrive_records_v1(body_data: TorsiondriveAddBody):
    limit = current_app.config["QCFRACTAL_CONFIG"].api_limits.add_records
    if len(body_data.initial_molecules) > limit:
        raise LimitExceededError(
            f"Cannot add {len(body_data.initial_molecules)} torsiondrive records - limit is {limit}"
        )

    return storage_socket.records.torsiondrive.add(
        initial_molecules=body_data.initial_molecules,
        td_spec=body_data.specification,
        as_service=body_data.as_service,
        tag=body_data.tag,
        priority=body_data.priority,
    )


@main.route("/v1/record/torsiondrive", methods=["GET"])
@main.route("/v1/record/torsiondrive/<int:record_id>", methods=["GET"])
@wrap_route(None, CommonGetProjURLParameters)
def get_torsiondrive_records_v1(record_id: Optional[int] = None, *, url_params: CommonGetProjURLParameters):
    limit = current_app.config["QCFRACTAL_CONFIG"].api_limits.get_records
    if url_params.id is not None and len(url_params.id) > limit:
        raise LimitExceededError(f"Cannot get {len(url_params.id)} torsiondrive records - limit is {limit}")

    return get_helper(
        record_id,
        url_params.id,
        url_params.include,
        None,
        url_params.missing_ok,
        storage_socket.records.torsiondrive.get,
    )


@main.route("/v1/record/torsiondrive/<int:record_id>/optimizations", methods=["GET"])
@wrap_route(None, CommonGetProjURLParameters)
def get_torsiondrive_optimizations_v1(record_id: int, *, url_params: CommonGetProjURLParameters):
    # adjust the includes/excludes to refer to the optimizations
    ch_includes, ch_excludes = prefix_projection(url_params, "optimizations")
    rec = storage_socket.records.torsiondrive.get([record_id], include=ch_includes, exclude=ch_excludes)
    return rec[0]["optimizations"]


@main.route("/v1/record/torsiondrive/<int:record_id>/initial_molecules", methods=["GET"])
@wrap_route(None, None)
def get_torsiondrive_initial_molecules_v1(record_id: int):
    rec = storage_socket.records.torsiondrive.get([record_id], include=["initial_molecules"])
    return rec[0]["initial_molecules"]


@main.route("/v1/record/torsiondrive/query", methods=["POST"])
@wrap_route(TorsiondriveQueryBody, None)
def query_torsiondrive_v1(body_data: TorsiondriveQueryBody):
    max_limit = current_app.config["QCFRACTAL_CONFIG"].api_limits.get_records
    body_data.limit = calculate_limit(max_limit, body_data.limit)

    return storage_socket.records.torsiondrive.query(body_data)

from typing import List

from flask import current_app

from qcfractal.app import main, wrap_route, storage_socket
from qcportal.base_models import CommonBulkGetBody, ProjURLParameters
from qcportal.exceptions import LimitExceededError
from qcportal.molecules import Molecule, MoleculeQueryFilters, MoleculeModifyBody
from qcportal.utils import calculate_limit


@main.route("/v1/molecules/<int:molecule_id>", methods=["GET"])
@wrap_route("READ")
def get_molecules_v1(molecule_id: int, url_params: ProjURLParameters):
    return storage_socket.molecules.get([molecule_id], url_params.include, url_params.exclude)[0]


@main.route("/v1/molecules/bulkGet", methods=["POST"])
@wrap_route("READ")
def bulk_get_molecules_v1(body_data: CommonBulkGetBody):
    limit = current_app.config["QCFRACTAL_CONFIG"].api_limits.get_molecules
    if len(body_data.ids) > limit:
        raise LimitExceededError(f"Cannot get {len(body_data.ids)} molecule records - limit is {limit}")

    return storage_socket.molecules.get(
        body_data.ids, body_data.include, body_data.exclude, missing_ok=body_data.missing_ok
    )


@main.route("/v1/molecules/<int:molecule_id>", methods=["DELETE"])
@wrap_route("DELETE")
def delete_molecules_v1(molecule_id: int):
    return storage_socket.molecules.delete([molecule_id])


@main.route("/v1/molecules/bulkDelete", methods=["POST"])
@wrap_route("DELETE")
def bulk_delete_molecules_v1(body_data: List[int]):
    return storage_socket.molecules.delete(body_data)


@main.route("/v1/molecules/<int:molecule_id>", methods=["PATCH"])
@wrap_route("WRITE")
def modify_molecules_v1(molecule_id: int, body_data: MoleculeModifyBody):
    return storage_socket.molecules.modify(
        molecule_id=molecule_id,
        name=body_data.name,
        comment=body_data.comment,
        identifiers=body_data.identifiers,
        overwrite_identifiers=body_data.overwrite_identifiers,
    )


@main.route("/v1/molecules/bulkCreate", methods=["POST"])
@wrap_route("WRITE")
def add_molecules_v1(body_data: List[Molecule]):
    limit = current_app.config["QCFRACTAL_CONFIG"].api_limits.add_molecules
    if len(body_data) > limit:
        raise LimitExceededError(f"Cannot add {len(body_data)} molecule records - limit is {limit}")

    return storage_socket.molecules.add(body_data)


@main.route("/v1/molecules/query", methods=["POST"])
@wrap_route("READ")
def query_molecules_v1(body_data: MoleculeQueryFilters):

    max_limit = current_app.config["QCFRACTAL_CONFIG"].api_limits.get_molecules
    body_data.limit = calculate_limit(max_limit, body_data.limit)

    return storage_socket.molecules.query(body_data)

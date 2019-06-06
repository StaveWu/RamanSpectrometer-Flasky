from flask import jsonify, request
from . import api
from ..detecting.repositories import SpectraRepository, ComponentModelRepository
from ..detecting.models import Spectrum, DetectResult
from ..utils import JsonWrapper


@api.route('/spectra')
def load_spectra():
    count = request.args.get('count', 8, type=int)
    spectra = SpectraRepository.find_by_timestamp_desc(count)
    return jsonify({
        'spectra': [spec.to_json() for spec in spectra]
    })


@api.route('/spectra/<int:id>')
def get_spectrum(id):
    spectrum = SpectraRepository.find_by_id(id)
    return jsonify(spectrum.to_json())


@api.route('/spectra', methods=['POST'])
def add_spectrum():
    spectrum = Spectrum.from_json(request.json)
    SpectraRepository.save_spectrum(spectrum)
    return jsonify(spectrum.to_json())


@api.route('/spectra/<int:id>', methods=['PATCH'])
def tag_spectrum(id):
    detect_result = DetectResult.from_json(request.json)

    spectrum = SpectraRepository.find_by_id(id)
    spectrum.set_component(detect_result)
    SpectraRepository.update_spectrum(spectrum)

    return jsonify({})


@api.route('/spectra/<int:id>/components', methods=['POST'])
def detect_components(id):
    wrapper = JsonWrapper(request.json)
    comp_ids_to_detect = wrapper.get_strict('compIds', type=list)

    # why we get spectrum from request instead of repository?
    # this is because some preprocessing action preformed in front end
    # and the performed result didn't save here
    d = request.json.copy()
    d['id'] = id
    spec = Spectrum.from_json(d)

    results = []
    for cid in comp_ids_to_detect:
        model = ComponentModelRepository.find_by_id(cid)
        results.append(model.predict(spec)[0])
    return jsonify({
        'results': [res.to_json() for res in results]
    })


@api.route('/spectra/components', methods=['POST'])
def batch_detect_components():
    wrapper = JsonWrapper(request.json)
    spec_ids = wrapper.get_strict('specIds', type=list)
    comp_ids = wrapper.get_strict('compIds', type=list)

    spectra = [SpectraRepository.find_by_id(spec_id) for spec_id in spec_ids]

    all_results = []
    for comp_id in comp_ids:
        model = ComponentModelRepository.find_by_id(comp_id)
        all_results.append(model.predict(spectra))

    response = []
    for spec_id, results in zip(spec_ids, all_results):
        response.append({
            'specId': spec_id,
            'results': [res.to_json() for res in results]
        })
    return jsonify(response)



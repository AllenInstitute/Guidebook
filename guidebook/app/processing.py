from flask import Blueprint, redirect, request, flash, render_template, url_for
from ..base import generate_proofreading_state
from .forms import SkeletonizeForm
import numpy as np

api_version = 0
url_prefix = f"/guidebook/v{api_version}"
bp = Blueprint("guidebook", __name__, url_prefix=url_prefix)

__version__ = "0.0.1"
DEFAULT_DATASTACK = 'minnie65_phase3_v1'


@bp.route("/")
def index():
    return f"Neuron Guidebook v. {__version__}"


@bp.route("skeletonize", methods=['GET', 'POST'])
def skeletonize_form():
    form = SkeletonizeForm()
    if form.validate_on_submit():
        datastack = DEFAULT_DATASTACK
        root_id = form.root_id.data
        root_loc_data = np.fromstring(
            form.root_location.data, count=3, dtype=np.int, sep=',')
        root_loc_formatted = '_'.join(map(str, root_loc_data))
        values = {'root_is_soma': form.root_is_soma.data,
                  'root_loc': root_loc_formatted}
        url = url_for('.generate_guidebook',
                      datastack=datastack, root_id=root_id, **values)
        flash(f'Generating proofreading link for {root_id}')

        return redirect(url)

    return render_template('skeletonize.html',
                           title='Neuron Guidebook',
                           form=form)


@bp.route("/datastack/<datastack>/root_id/<int:root_id>", methods=["GET", "POST"])
def generate_guidebook(datastack, root_id,):
    root_is_soma = request.args.get('root_is_soma', False)
    root_loc = request.args.get('root_loc', None)
    if root_loc is not None:
        root_loc = np.array(root_loc.split('_')).astype(
            int) * np.array([4, 4, 40])
        print(f'Root location is: {root_loc}')
    state = generate_proofreading_state(
        datastack, int(root_id), root_is_soma=root_is_soma, root_loc=root_loc,  return_as='url')
    return redirect(state, code=302)

# BPTK Model Library

Welcome to the BPTK Model Library, a small but growing collection of System Dynamics models and Agent-based models built using the [Business Prototyping Toolkit for Python](https://bptk.transentis.com)

* __[Introduction to BPTK](./bptk_intro/intro_to_bptk.ipynb).__ An overview of the BPTK framework that illustrates how to built System Dynamics models, Agent-based models and hybrid SD-ABM models.
* __[Bass Diffusion Model](./bass_diffusion/bptk_py_bass_diffusion.ipynb).__ The classic [Bass Diffusion Model](https://en.wikipedia.org/wiki/Bass_diffusion_model) that is used to explain the dynamics of introductiong a new product or service into a market.
* __[Competitive Pricing](./competitive_pricing/competitive_pricing_dynamics_sd_dsl.ipynb)__ A neat little model that can be used to understand pricing dynamics.
* __[Customer Acquisition](./customer_acquisition/customer_acquisition.ipynb).__ A model that analyses the effects of referral marketing on customer acquisition.
* __[Make Your Professional Service Firm Grow](./make_your_psf_grow/sddsl/make_your_psf_grow_part_1_sddsl.ipynb).__ A model that analyses growth strategies in professional service firms.

## Installing

Open your command line in an appropriate folder and clone this repository: git clone http://github.com/transentis/bptk_intro.git

* CD into the directory: cd bptk_intro
* Set up a virtual environment: python3 -m venv venv
* Activate the enviroment: source venv\bin\activate
* Install the required packages: pip install -r requirements.txt
* Start jupyter: `jupyter lab``
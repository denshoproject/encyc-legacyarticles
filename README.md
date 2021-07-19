# encyc-legacyarticles

In 2020 and 2021, several articles in the Densho Encyclopedia were replaced with newer versions; however, there was a need to continue making the original articles accessible. 

In order to support this, static versions of the legacy articles were created. The `/content/` directory in this repo contains both the html files and the supporting images. The `getlegacycontent.py` script is used to retrieve the raw html and thumbnail images from the production site cache. The `processlegacycontent.py` script performs a variety of transformations to the retrieved html pages to prep them for deployment as legacy article pages.  

In the production environment, the static files are hosted at: `https://encyclopedia.densho.org/media/encyc-legacy`

# explore-cogs

Notebooks for exploring Earth Observation Data in Cloud-Optimized GeoTIFFs (COGs)

Explore using [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/abarciauskas-bgse/explore-cogs/master).

Note: The mybinder image build takes a few minutes, so please be patient 😺.

If you have docker installed, you can also pull an image run the code locally:

```bash
docker pull aimeeb2/explore-cogs
docker run -d -p 8888:8888 --name explore-cogs explore-cogs:latest 
open http://localhost:8888
```

## Local development

```bash
docker build -t explore-cogs:latest -f Dockerfile.base .
# docker tag explore-cogs:latest aimeeb2/explore-cogs:latest
# docker push aimeeb2/explore-cogs:latest
```

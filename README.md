# explore-cogs

Notebooks for exploring Earth Observation Data in Cloud-Optimized GeoTIFFs (COGs)

Explore using [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/abarciauskas-bgse/explore-cogs/master). Note: the first time you build the image in mybinder it might time out, so please be patient and try again 😺.

If you have docker installed, you can also pull an image run the code locally:

```bash
docker pull aimeeb2/cog-explore
docker run -d -p 8888:8888 cog-explore:latest --name cog-explore
open http://localhost:8888
```

## Local development

```bash
docker build -t cog-explore:latest .
# docker tag cog-explore:latest aimeeb2/explore-cog:latest
# docker push aimeeb2/explore-cog:latest
```

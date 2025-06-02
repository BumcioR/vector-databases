Vector databases

**Necessary software**

- [Docker and Docker Compose](https://docs.docker.com/engine/install/),
  also [see those post-installation notes](https://docs.docker.com/engine/install/linux-postinstall/)
- Postgres client, e.g. `sudo apt install postgresql-client`
  ([more details](https://askubuntu.com/questions/1040765/how-to-install-psql-without-postgres))
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.11

**Data**

We will be using [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)
about games published on Steam, as well as
[Amazon Berkeley Objects (ABO) Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html)
with data about objects available in the Amazon store.

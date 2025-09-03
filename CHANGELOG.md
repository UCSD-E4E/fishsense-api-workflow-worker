# CHANGELOG

<!-- version list -->

## v1.5.6 (2025-09-03)

### Bug Fixes

- Pydantic allow null user ids
  ([`275fd59`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/275fd59b4fb70bbc0eb1783d68308828f19b7c60))


## v1.5.5 (2025-09-03)

### Bug Fixes

- Failed run for collecting user b/c we did not specify a url
  ([`a5c5a3f`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/a5c5a3f8da014623ad30d8b90e867332ac05ceac))


## v1.5.4 (2025-09-03)

### Bug Fixes

- Please pylint
  ([`4354ca3`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/4354ca36bd7e9752f053c7d64ffc3a42950b0055))

- Pydantic doesn't like the label studio api type
  ([`3be187d`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/3be187d313646aeac72a4f475b9e11ba7cccd87d))


## v1.5.3 (2025-09-03)

### Bug Fixes

- Pydantic errors with label studio api
  ([`20f0507`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/20f0507d24cfc646fe16013a8aec115c18dc9e6c))


## v1.5.2 (2025-09-03)

### Bug Fixes

- Move label studio import into class.
  ([`79c158b`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/79c158b6cb61e619ffd47c40559454ba35859ea6))

- Please pylint
  ([`233d5b0`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/233d5b092ea94aa43a7edf4da1bf60373c38e22e))


## v1.5.1 (2025-09-03)

### Bug Fixes

- Pylint errors
  ([`461e2f8`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/461e2f88e4d2fe518ea90808686320987bd9d326))


## v1.5.0 (2025-09-02)

### Features

- Add tqdm
  ([`9e8e52b`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/9e8e52bf9e2096205a5fc0e0986529e5f5b29caa))


## v1.4.1 (2025-09-02)

### Bug Fixes

- Add executor for sync activities
  ([`11ec9b9`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/11ec9b9bbdb3b7d3ff487f89ede2074d1b25424c))


## v1.4.0 (2025-09-02)

### Bug Fixes

- Don't initialize the database in a loop
  ([`a8e734d`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/a8e734d5e77ad4c7a2124f6d0666442857c427bb))

- Ensure that we set users for labels
  ([`7bd6465`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/7bd6465eeac3be451637de61cac86ea7a5f62a72))

- Other copilot related errors
  ([`451a20e`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/451a20e6eb9c8ca70cdc9c61a7a7b5cb45fa53a3))

- Run uv sync when starting container
  ([`439faf4`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/439faf4ef84497191129ef63661896b8d569959b))

### Chores

- Appease pylint
  ([`41cc142`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/41cc142c3d2a7dce7babcbc99966907e9db47ad8))

- Cleanup unused code.
  ([`26b1ac1`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/26b1ac174a67a0fc7051f27ea85f7c3a765158f2))

- Please pylint
  ([`79a1857`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/79a185776d94662e89677149e4b271c54cf6aade))

### Features

- Add head tail label
  ([`987a1ae`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/987a1ae2d90202a7cad831ffac500abc11bc4e1e))

- Add users to database
  ([`941958a`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/941958a9eee1870dbaa1f7ea1555e78d7957dbce))

- Can initialize database
  ([`8dc99ba`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/8dc99ba6a7e38b8803c8a2bcf1c2186a6581a664))

- Initialize database
  ([`12df08d`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/12df08df99ab1c74b1c7d2a2208ee95d8cd4d0ad))

- Introduce postgres to the dev environment
  ([`00966ec`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/00966ec6f28ae2a6121c55f492149fcb6ee6f2de))

- Start of dev container
  ([`730c780`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/730c780bf5669e463cc5f5a3c18cb90cd2e071a1))

- Support cameras, dives, and images fully
  ([`9e5bc64`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/9e5bc64ac43324d9456c2669cac9a98df20f763a))

- Support head tail labels in new database
  ([`6492143`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/6492143ddd49f75db2889d6f88a091c62806a674))

- Sync users from label studio
  ([`a5cee52`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/a5cee522413b8e1e1b6d22dfd10dc420bb52c69e))

- Update activity to use new orm database layer
  ([`83b94df`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/83b94df2175d4d61e3a9bc68f644e60cb9ce6c9b))


## v1.3.1 (2025-08-22)

### Bug Fixes

- Label studio percentages are in whole numbers.
  ([`349f5d2`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/349f5d28cf52cbcae80de4af5c1a4749914aec5a))


## v1.3.0 (2025-08-22)

### Bug Fixes

- Pylint
  ([`841613c`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/841613ccde2c34272746b3d34118b88b49696fb3))

### Chores

- Fix pylint
  ([`ab068ea`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/ab068ea656c777e8c3ea9357c2001a850da727e3))

### Features

- Collect head tail labels from label studio
  ([`51d6037`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/51d6037df33075ff0bb8c2085574d47a0e464241))

- Insert headtail labels into postgres
  ([`c1d52f3`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/c1d52f33cdec5010c6bb2ed1e20b0a7c2e68e6da))


## v1.2.4 (2025-08-21)

### Bug Fixes

- Sql file name
  ([`3ec1a34`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/3ec1a34609e6a7c485278b0bf69e1c6e2a4fc102))


## v1.2.3 (2025-08-21)

### Bug Fixes

- Pylint error
  ([`fcfad9b`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/fcfad9bafd15e3ebe1cfe9ecd2d83512df93c945))

- Use the full path if running in docker
  ([`b688b07`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/b688b0709e636f2a72c72dc3ef77e52d2558cad9))


## v1.2.2 (2025-08-21)

### Bug Fixes

- Sql path issue in docker container
  ([`016fba7`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/016fba7cf9e5534f3a5d81dbd9df1ab0abdc7a11))


## v1.2.1 (2025-08-21)

### Bug Fixes

- Add missing sql scripts
  ([`9180389`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/918038931c2deaa4950ff9d3921047643a63e730))


## v1.2.0 (2025-08-21)

### Features

- Implement label studio laser activity
  ([`92f57f9`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/92f57f9d7f54e02a8080f01d4b648d28b84132b8))

- Introduce logging
  ([`f527c18`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/f527c18b7a6f0dd3911eee57e5075eecc229b1cf))

- Write to postgres
  ([`0b40ed0`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/0b40ed0219e73a313d10332c2ff211efd4d54073))


## v1.1.0 (2025-08-21)

### Features

- Add validators to settings
  ([`1ba107b`](https://github.com/UCSD-E4E/fishsense-api-workflow-worker/commit/1ba107bc9b5cf6f998fc14ee59239f850aabbf80))


## v1.0.0 (2025-08-21)

- Initial Release

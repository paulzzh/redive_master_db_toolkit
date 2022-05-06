# redive_master_db_toolkit
Tools to crawl, dump and rebuild the master db for PCRD.

# What's this?
- guess.py: guess trustversion and download the AssetBundles.
- diff.py: unpack the AssetBundles and dump the master db to sql.
- commit.py: then commit the datebase difference.
- push.py: update remote.

# How to generate master db file?
- build.py: turn sql files into db file.
- If you want an old version, run `git reset --hard <commit>` in the diff repo folder, and run build.py again.

# Thanks https://github.com/esterTion/unity-texture-toolkit

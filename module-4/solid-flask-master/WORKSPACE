workspace(name = "solid_flask")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "rules_python",
    commit = "a16432752ef33b98530f05ca86375b42059b23c0",
    remote = "https://github.com/bazelbuild/rules_python",
    shallow_since = "1608774260 +1100",
)

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "my_deps",
    requirements = "//:requirements.txt",
)

import aiohttp.web
import argparse
import logging

from kube_web import __version__
from .web import get_app
from .cluster_manager import ClusterManager


logger = logging.getLogger(__name__)


def main(argv=None):

    parser = argparse.ArgumentParser(description=f"Kubernetes Web View v{__version__}")
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="TCP port to start webserver on (default: 8080)",
    )
    parser.add_argument(
        "--version", action="version", version=f"kube-web-view {__version__}"
    )
    parser.add_argument("--kubeconfig-path", help="Path to ~/.kube/config file")
    parser.add_argument(
        "--show-container-logs",
        action="store_true",
        help="Enable container logs (hidden by default as they can contain sensitive information)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Run in debugging mode (log more)"
    )

    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    config_str = ", ".join(f"{k}={v}" for k, v in sorted(vars(args).items()))
    logger.info(f"Kubernetes Web View v{__version__} started with {config_str}")

    cluster_manager = ClusterManager(args.kubeconfig_path)
    app = get_app(cluster_manager, args)
    aiohttp.web.run_app(app, port=args.port)
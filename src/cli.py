from typing import Dict, Any, List
import click
import yaml
from pathlib import Path
from core import data_load, draw, similarity, statistics, divide, timestamp_get
from core.config import Config


def load_config(config_path: Path) -> Config | Dict[str, Config]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config YAML file
    """
    register, check = None, None
    with open(config_path) as f:
        config_data = yaml.safe_load(f)
        if not config_data:
            raise click.BadParameter("No configuration data found")
        if config_data.__contains__('register'):
            register = Config(**config_data['register'])
        if config_data.__contains__('check'):
            check = Config(**config_data['check'])
    return Config(**config_data) if register is None and check is None else {'register': register, 'check': check}

def process_data(config: Config) -> List[List[float]]:
    """Process data according to configuration"""

    data = None
    """if need to divide"""
    if (
        config.divide_input_path and 
        config.divide_output_prefix and
        config.divide_filter
    ):
        divide.split_csv(
            config.divide_input_path,
            config.divide_output_prefix,
            config.divide_filter
        )
        config.load_base_path = str(Path(config.divide_output_prefix).parent)
    
    """load data"""
    if config.load_base_path:
        data = data_load.load_csv_files(
            base_path=config.load_base_path,
            start_idx=config.load_start_idx or 2,
            end_idx=config.load_end_idx or 102,
            file_pattern=config.load_file_pattern or 'output_{}.csv'
        )
    else:
        raise click.BadParameter("No data path specified")
    
    """get time series data"""
    if (
        data and 
        config.timestamp_pattern
    ):
        return [timestamp_get.get_timestamps(
            df_i,
            config.timestamp_pattern
        ) for df_i in data.values()]

    elif not data:
        raise click.BadParameter("No data loaded")
    else:
        raise click.BadParameter("No timestamp pattern specified")

def create_visualizations(data: Dict[str, Any], config: Config) -> None:
    """Create visualizations based on processed data"""
    draw.draw(
        identifiers=list(data.values()),
        **config.plot_settings
    )

@click.group()
@click.option(
    '--config',
    '-c',
    type=click.Path(exists=True),
    default='config.yaml',
    help='Path to configuration file'
)

@click.pass_context
def cli(ctx: click.Context, config: str) -> None:
    """USB Data Analysis CLI"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(Path(config))


@cli.command()
@click.pass_context
def register(ctx: click.Context) -> None:
    """Register USB data"""
    distance_paths = []
    origin_time_series = []
    dtw_mapping = []
    finger = []

    config:Config = ctx.obj['config']['register'] if ctx.obj['config'].__contains__('register') else ctx.obj['config']
    timestamp_data = process_data(config)
    
    """"draw time series"""
    if timestamp_data and config.draw_save_path:
        draw.draw(
            identifiers=timestamp_data,
            title=config.draw_title or 'Time Series',
            xlabel=config.draw_xlabel or 'Time',
            ylabel=config.draw_ylabel or 'Value',
            save_path=config.draw_save_path
        )

    """calculate similarity"""
    if timestamp_data:
        origin_time_series = timestamp_data[0]
        distance_paths = [similarity.dtw_distance_with_path(
            ts_i,
            origin_time_series
        )[1] for ts_i in timestamp_data]

        dtw_mapping = [[] for _ in range(len(origin_time_series))]
        for idx,  path in enumerate(distance_paths):
            for num in path:
                dtw_mapping[num[1]].append(timestamp_data[idx][num[0]])
        
        finger = [statistics.concentrated_range(ts_i)[1] for ts_i in dtw_mapping if ts_i]
        print (f'Finger:{finger}')

        finger_distance = [similarity.dtw_distance_with_path(
            ts_i,
            finger
        )[0] for ts_i in timestamp_data]

        print(f'Suggest range: {statistics.concentrated_range(finger_distance, threshold=3, use_robust=True)[0]}')


@cli.command()
@click.pass_context
def check(ctx: click.Context) -> None:
    """Check USB data"""
    config: Config = ctx.obj['config']['check'] if ctx.obj['config'].__contains__('check') else ctx.obj['config']
    timestamp_data = process_data(config)
    finger = config.finger
    check_range = config.check_range

    if timestamp_data and finger and check_range:
        distance = [similarity.dtw_distance_with_path(
            ts_i,
            finger
        )[0] for ts_i in timestamp_data]
        print(f'check pass rate:{len([d for d in distance if d < check_range[1] and d > check_range[0]]) / len(distance) : .2%}')


if __name__ == '__main__':
    cli(obj={})
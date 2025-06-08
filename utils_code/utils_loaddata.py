import zipfile
from pathlib import Path

import pandas as pd


from typing import Union



def read_zip_csv(
    filepath: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Read a CSV file stored inside a ZIP archive.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Combined path to the ZIP archive and the inner CSV file, separated by '!'
        (e.g. '/path/to/archive.zip!data.csv' or Path('/path/to/archive.zip!data.csv')).
    **kwargs :
        Additional keyword arguments passed through to `pandas.read_csv`
        (e.g. `sep=',', header=0, dtype={'col': str}`).

    Returns
    -------
    pd.DataFrame
        Contents of the specified CSV file as a DataFrame.

    Raises
    ------
    ValueError
        If `filepath` does not include the '!' delimiter.
    FileNotFoundError
        If the ZIP archive doesn't exist or the CSV file isn't found inside it.
    """
    # Ensure proper delimiter
    filepath = str(filepath)
    if '!' not in filepath:
        raise ValueError("`filepath` must be in the format 'archive.zip!file.csv'")

    zip_path_str, csv_name = filepath.split('!', 1)
    zip_path = Path(zip_path_str)

    # Check ZIP archive exists
    if not zip_path.is_file():
        raise FileNotFoundError(f"ZIP archive not found: {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Check CSV exists inside archive
        if csv_name not in zf.namelist():
            raise FileNotFoundError(f"'{csv_name}' not found in archive '{zip_path.name}'")

        with zf.open(csv_name) as f:
            return pd.read_csv(f, **kwargs)
# ==========================================================================================================
def test_datastore_file_setting():
    """
    Test the setting of the datastore file path.
    """
    import tempfile
    from nfl_analytics._local_storage import set_datastore_path, _get_datastore_path

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set the temporary directory as the datastore path
        set_datastore_path(temp_dir)

        # Check if the path is set correctly
        assert _get_datastore_path() == temp_dir


def test_create_subdir():
    """
    Test the creation of a subdirectory in the datastore path.
    """
    import os
    from nfl_analytics._local_storage import set_datastore_path, _create_subdir
    import tempfile

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set the temporary directory as the datastore path
        set_datastore_path(temp_dir)

        # Create a subdirectory
        subdir_name = "test_subdir1/test_subdir2/"
        _create_subdir(subdir_name)

        # Check if the subdirectory is created
        subdir_path = os.path.join(temp_dir, subdir_name)
        assert os.path.exists(subdir_path)


def test_frame_io():
    """
    Test the dumping and loading of a DataFrame to/from the datastore.
    """
    import pandas as pd
    from nfl_analytics._local_storage import set_datastore_path, dump_frame, load_frame, file_exists
    import tempfile

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set the temporary directory as the datastore path
        set_datastore_path(temp_dir)

        # Create a sample DataFrame
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        subdir_name = "test_subdir1/test_subdir2/"
        filename = "test_frame.csv"

        # Make sure the file does not exist before dumping
        assert not file_exists(subdir_name, filename)

        # Dump the DataFrame to the datastore
        dump_frame(df, subdir_name, filename)

        # Make sure the file exists after dumping
        assert file_exists(subdir_name, filename)

        # Load the DataFrame from the datastore
        loaded_df = load_frame(subdir_name, filename)

        # Check if the loaded DataFrame is equal to the original DataFrame
        assert df.equals(loaded_df)

# Useful Pandas Functions

# Just some functions I wrote out to streamline the pandas reading
# and writing process.

import pandas as pd

def GenerateMasterList(FileDirectory):
    """
    Reads in the file inputted and outputs it as a pandas DF. It 
    assumes there is no header row.
    """
    return (pd.read_csv(FileDirectory, delim_whitespace = True,
                        header = None, index_col=None))

def GenerateMasterListWithHeader(FileDirectory):
    """Reads in the file with a header"""
    return  (pd.read_csv(FileDirectory, delim_whitespace = False))

def WriteTo(DataFrame, Directory):
    """Writes dataframe to the directory"""
    DataFrame.to_csv(Directory, index = False, header = None)

def WriteToWithHeader(DataFrame, Directory):
    """Writes dataframe to the directory with a header"""
    DataFrame.to_csv(Directory, index = False)

def TurnDFintoMatrix(DataFrame):
    """Converts a dataframe to a numpy matrix"""
    return DataFrame.as_matrix(columns = None)

def binaryVectorization(DataFrame):
    """
    Takes a dataframe of integers ranged from 0 to n, and creates a
    n-dimensional binary vector.
    """
    width = int(DataFrame.max())
    length = DataFrame.shape[0]

    binaryVector = pd.DataFrame(0,index=range(length),
                                columns=range(width))
    for i in range(length):
        binaryVector.iloc[i,DataFrame.iloc[i]-1] = 1

    return binaryVector

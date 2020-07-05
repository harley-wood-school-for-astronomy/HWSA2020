#!/usr/bin/env python
################################
# Author: Manodeep Sinha
# Harley-Wood School, July 2020
################################


def your_custom_processing_func(input_fname, rank=0,
                                outputfilebase='linecounting_results'):
    numlines = None
    try:
        with open(input_fname, 'r') as f:
            numlines = 0
            for line in f:
                numlines += 1
    except IOError:
        print(f"[Rank={rank}]: Did not find input file = '{input_fname}'")
        pass

    # Now write the reusult
    outputfilename = f"{outputfilebase}_{rank}.csv"
    with open(outputfilename, 'a') as f:
        f.write(f"{input_fname}, {numlines}\n")

    return


def distributed_processing(filenames, processing_func=None,
                           outputfilebase='linecounting_results'):
    import sys
    import os
    import time

    tstart = time.perf_counter()
    rank = 0
    ntasks = 1
    MPI = None
    comm = None
    try:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        ntasks = comm.Get_size()
    except ImportError:
        pass

    # Protect against the case where a single
    # file was passsed
    if not isinstance(filenames, (list, tuple)):
        filenames = [filenames]

    sys.stdout.flush()
    nfiles = len(filenames)
    if nfiles < ntasks:
        print(f"[Rank={rank}]: Nfiles = {nfiles} < total tasks = {ntasks}. "
            "Some tasks will not have any work assigned (and will be idle)")

    if rank == 0:
        # Delete the output results file, otherwise
        # the file will keep getting appended to
        for itask in range(ntasks):
            try:
                os.remove(f"{outputfilebase}_{itask}.csv")
            except OSError:
                pass

        print(f"[Rank={rank}]: Converting nfiles = {nfiles} over "\
              f"ntasks = {ntasks}...")
    if comm:
        # wait for rank==0 to reach here
        # so that the new output files are created after
        # the old files are deleted
        comm.Barrier()

    # Convert files in MPI parallel (if requested)
    # the range will produce filenum starting with "rank"
    # and then incrementing by "ntasks" all the way upto
    # and inclusive of [nfiles-1]. That is, the range [0, nfiles-1]
    # will be uniquely distributed over ntasks.
    for filenum in range(rank, nfiles, ntasks):
        processing_func(filenames[filenum], rank, outputfilebase)

    # The barrier is only essential so that the total time printed
    # out on rank==0 is correct.
    if comm:
        comm.Barrier()

    if rank == 0:
        t1 = time.perf_counter()
        print(f"[Rank={rank}]: Converting nfiles = {nfiles} over ntasks = "\
              f"{ntasks}...done. Time taken = {t1-tstart:0.3f} seconds")

    return True


if __name__ == "__main__":
    import glob
    try:
        temp_filebase
    except NameError:
        temp_filebase = "temp_xxxxxx"

    # Prefer to sort the results from glob (famous bugs have occurred)
    filenames = sorted(glob.glob(f"./{temp_filebase}_*.txt"))
    distributed_processing(filenames, your_custom_processing_func)

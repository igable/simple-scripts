#!/bin/env python

import csv
import commands
import datetime
import logging
import os
import sys

class Execution( object ):
    def __init__( self ):
        self.logger = logging.getLogger("Execution")

    def execute( self, cmd ):
        """Executes the command and prints error results"""

        result = commands.getstatusoutput( cmd )

        if result[0] == 0:
            return result[1]
        else:
            self.logger.error( result )
            return None
            
class Condor( object ):
    def __init__( self ):
        self.logger = logging.getLogger("Condor")
        self.data = []
        self.binned = None

    def Count( self, cmd ):
        self.logger.debug("Starting count")

        self.logger.debug("Getting Condor History Data")
        history_result = Execution()
        self.data.append( history_result.execute( cmd ).split() )

    def OutputDates( self, bin_size ):
        csvfile = csv.writer( open("job_completion_count_by_date.csv", "w") )

        for ii in sorted(self.binned.keys()):
            dt = datetime.date.fromtimestamp(ii*bin_size)
            dt_count = self.binned[ii]
            print "%s %d" % ( dt, dt_count )
            csvfile.writerow( [dt, dt_count] )

    def Rebin( self, bin_factor ):
        self.logger.debug("Rebin")
        self.binned = {}
        for ii in self.data:
            for jj in ii:
                bin_number = int( int(jj) / bin_factor)
                if bin_number in self.binned:
                    self.binned[bin_number] = self.binned[bin_number] + 1
                else:
                    self.binned[bin_number] = 1
            
    def OutputJobLength( self ):
        csvfile = csv.writer( open("jobs_completed_count_by_execution_length.csv", "w") )

        for ii in sorted(self.binned):
            print "%d %d" % ( ii, self.binned[ii] )
            csvfile.writerow( [ii, self.binned[ii]] )
        
class StartTime( object ):
    def __init__( self ):
        self.logger = logging.getLogger("StartTime")

    def Get( self ): 
        date_cmd = "date -d '-365 days' +%s"
        execution = Execution()
        return execution.execute(date_cmd)
        
def main():
    logging.basicConfig()
    logging.root.setLevel( logging.DEBUG )
    logger = logging.root

    startTime = StartTime()
    start_time = startTime.Get()
    print start_time
    logger.debug( "Start time is %d" % int(start_time) )

    job_completion = Condor()
    job_length = Condor()

    listing = os.listdir("./")
    for ii in listing:
        if ii.startswith( "history" ):
            logger.debug( "History file %s" % ii )
            job_completion_cmd = \
                "condor_history -f %s -constraint 'CompletionDate>=%s' -format '%%i\n' CompletionDate" \
                % ( ii, start_time )
            job_count_cmd = \
                "condor_history -f %s -constraint 'CompletionDate>=%s' -format '%%i\n' RemoteWallClockTime" \
                % ( ii, start_time )
            job_completion.Count( job_completion_cmd )
            job_length.Count( job_count_cmd )

    # bin job completion rate by day
    #
    job_completion.Rebin( 86400 )
    #
    # bin completed job length by hour
    #
    job_length.Rebin( 3600 ) 

    job_completion.OutputDates( 86400 )
    job_length.OutputJobLength()

    sys.exit(0)


if __name__ == "__main__":
        main()



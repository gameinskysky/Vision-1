#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $1.0.0$

## script to convert bag file into csv file for postprocessing
#
# original version by Nick Speal, May 2013, at McGill University's 
# Aerospace Mechatronics Laboratory www.speal.ca
# adapted by Julian Surber, Oktober 2015, at ETH Zurich


import rosbag, sys, csv
import time
import string
import shutil #for file management, copy filemport rosbag

#folder = '/home/julian/catkin_additions/log'
#filename_bag = 'rovio_table_p22021.bag'
#topic_name = ['/rovio/transform']

if (len(sys.argv) == 3):
	bag_file = sys.argv[1]
	topic_name = sys.argv[2]	
else:
	print "invalid number of arguments:   " + str(len(sys.argv))
	print "should be 3: 'bag_to_csv.py' and 'filename.bag' and 'topic_name'"
	sys.exit(1)
	

bag = rosbag.Bag(bag_file)
bag_contents = bag.read_messages(topics=topic_name)
bag_name = bag.filename

csv_file = string.rstrip(bag_file, ".bag") + '.csv'
with open(csv_file,'w+') as csvfile:
	filewriter = csv.writer(csvfile, delimiter = ',')
	firstIteration = True	#allows header row
	for subtopic, msg, t in bag_contents:
		msgString = str(msg)
		msgList = string.split(msgString, '\n')
		instantaneousListOfData = []
		for nameValuePair in msgList:
			splitPair = string.split(nameValuePair, ':')
			for i in range(len(splitPair)):	#should be 0 to 1
				splitPair[i] = string.strip(splitPair[i])
				if i==1:
					instantaneousListOfData.append(splitPair)
		#write the first row from the first element of each pair
		if firstIteration:	# header
			headers = ["rosbagTimestamp"]	#first column header
			for pair in instantaneousListOfData:
				headers.append(pair[0])
			filewriter.writerow(headers)
			firstIteration = False

		# write the value from each pair to the file
		values = [str(t)]	#first column will have rosbag timestamp
		for pair in instantaneousListOfData:
			values.append(pair[1])
		filewriter.writerow(values)

bag.close()

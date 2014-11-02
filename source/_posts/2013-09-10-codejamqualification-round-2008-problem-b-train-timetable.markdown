---
layout: post
title: '[CodeJam]Qualification Round 2008 Problem B. Train Timetable'
categories:
- 技术
tags: [CodeJam]
published: true
comments: true
---
<p><a href="http://code.google.com/codejam/contest/32013/dashboard#s=p1&amp;a=1">http://code.google.com/codejam/contest/32013/dashboard#s=p1&amp;a=1</a></p>

<p>Problem</p>

<p>A train line has two stations on it, A and B. Trains can take trips from A to B or from B to A multiple times during a day. When a train arrives at B from A (or arrives at A from B), it needs a certain amount of time before it is ready to take the return journey - this is the<i>turnaround time</i>. For example, if a train arrives at 12:00 and the turnaround time is 0 minutes, it can leave immediately, at 12:00.</p>

<p>A train timetable specifies departure and arrival time of all trips between A and B. The train company needs to know how many trains have to start the day at A and B in order to make the timetable work: whenever a train is supposed to leave A or B, there must actually be one there ready to go. There are passing sections on the track, so trains don't necessarily arrive in the same order that they leave. Trains may not travel on trips that do not appear on the schedule.</p>

<p>Input</p>

<p>&nbsp;</p>

<p>The first line of input gives the number of cases, <b>N</b>. <b>N</b> test cases follow.</p>

<p>&nbsp;</p>

<p>Each case contains a number of lines. The first line is the turnaround time, <b>T</b>, in minutes. The next line has two numbers on it, <b>NA</b> and <b>NB</b>. <b>NA</b> is the number of trips from A to B, and <b>NB</b> is the number of trips from B to A. Then there are <b>NA</b> lines giving the details of the trips from A to B.</p>

<p>&nbsp;</p>

<p>Each line contains two fields, giving the HH:MM departure and arrival time for that trip. The departure time for each trip will be earlier than the arrival time. All arrivals and departures occur on the same day. The trips may appear in any order - they are not necessarily sorted by time. The hour and minute values are both two digits, zero-padded, and are on a 24-hour clock (00:00 through 23:59).</p>

<p>&nbsp;</p>

<p>After these <b>NA</b> lines, there are <b>NB</b> lines giving the departure and arrival times for the trips from B to A.</p>

<p>&nbsp;</p>

<p>Output</p>

<p>For each test case, output one line containing "Case #<b>x</b>: " followed by the number of trains that must start at A and the number of trains that must start at B.</p>

<p>&nbsp;</p>

<p>Limits</p>

<p>1 ≤ <b>N</b> ≤ 100</p>

<p>Small dataset</p>

<p>0 ≤ <b>NA</b>, <b>NB</b> ≤ 20</p>

<p>0 ≤ <b>T</b> ≤ 5</p>

<p>Large dataset</p>

<p>0 ≤ <b>NA</b>, <b>NB</b> ≤ 100</p>

<p>0 ≤ <b>T</b> ≤ 60</p>

<p>Sample
<div>
<table>
<tbody>
<tr>
<td>Input</td>
<td>Output</td>
</tr>
<tr>
<td><code><code>2<br />
5
3 2<br />
09:00 12:00<br />
10:00 13:00<br />
11:00 12:30<br />
12:02 15:00<br />
09:00 10:30<br />
2
2 0<br />
09:00 09:01<br />
12:00 12:02</code></code>&nbsp;</td>
<td><code><code>Case #1: 2 2<br />
Case #2: 2 0</code></code>&nbsp;</td>
</tr>
</tbody>
</table>
&nbsp;</div></p>

<p>This problem can be solved with a greedy strategy. The simplest way to do this is by scanning through a list of all the trips, sorted by departure time, and keeping track of the set of trains that will be available at each station, and when they will be ready to take a trip.</p>

<p>When we examine a trip, we see if there will be a train ready at the departure station by the departure time. If there is, then we remove that train from the list of available trains. If there is not, then our solution will need one new train added for the departure station. Then we compute when the train taking this trip will be ready at the other station for another trip, and add this train to the set of available trains at the other station. If a train leaves station A at 12:00 and arrives at station B at 13:00, with a 5-minute turnaround time, it will be available for a return journey from B to A at 13:05.</p>

<p>We need to be able to efficiently identify the earliest a train can leave from a station; and update this set of available trains by adding new trains or removing the earliest train. This can be done using a heap data structure for each station.</p>

<p>Sample Python code provided below that solves a test case for this problem:
<pre lang="python" colla="+">def SolveCase(case_index, case):
  T, (tripsa, tripsb) = case
  trips = []
  for trip in tripsa:
    trips.append([trip[0], trip[1], 0])
  for trip in tripsb:
    trips.append([trip[0], trip[1], 1])</pre></p>

<p>  trips.sort()</p>

<p>  start = [0, 0]<br />
  trains = [[], []]</p>

<p>  for trip in trips:<br />
    d = trip[2]<br />
    if trains[d] and trains[d][0] &lt;= trip[0]:<br />
      # We're using the earliest train available, and<br />
      # we have to delete it from this station's trains.<br />
      heappop(trains[d])<br />
    else:<br />
      # No train was available for the current trip,<br />
      # so we're adding one.<br />
      start[d] += 1<br />
    # We add an available train in the arriving station at the<br />
    # time of arrival plus the turnaround time.<br />
    heappush(trains[1 - d], trip[1] + T)</p>

<p>  print "Case #%d: %d %d" % (case_index, start[0], start[1])

Luckily Python has methods that implement the heap data structure operations. This solution takes O(n log n) time, where n is the total number of trips, because at each trip we do at most one insert or one delete operation from the heaps, and heap operations take O(log n) time.</p>

<p></p>

<p><pre lang="cpp" colla="+" /></p>

<p>//<br />
//  main.cpp<br />
//  CodeJamProject<br />
//<br />
//  Created by Jiang, Nan on 8/26/13.<br />
//  Copyright (c) 2013 Jiang, Nan. All rights reserved.<br />
//</p>

<p>//#include <iostream>
#include <stdio.h>
#include <map>
#include <vector>
using namespace std;</vector></map></stdio.h></iostream></p>

<p>struct Trip{<br />
    int startTime;<br />
    int arriveTime;<br />
    int from;<br />
};</p>

<p>bool sortByMe(Trip& t1, Trip& t2){<br />
    return t1.startTime < t2.startTime;<br />
}</p>

<p>int main(int argc, const char * argv[])<br />
{
    freopen("/Users/jiangnan/Develop/Code Jam/2008/CodeJamProject/CodeJamProject/B-large-practice.in.txt", "r", stdin);<br />
    freopen("/Users/jiangnan/Develop/Code Jam/2008/CodeJamProject/CodeJamProject/B-large-practice.out.txt", "w", stdout);<br />
    <br />
    int numCase;<br />
    scanf("%d", &numCase);<br />
    for (int c = 0; c < numCase; c++) {<br />
        int t = 0, na = 0, nb = 0;<br />
        scanf("%d", &t);<br />
        scanf("%d %d", &na, &nb);<br />
        vector<trip> trips;<br />
        for (int i = 0; i < na + nb; i++) {<br />
            int hh = 0, mm = 0;<br />
            scanf("%d:%d", &hh, &mm);<br />
            int start = hh * 60 + mm;<br />
            scanf("%d:%d", &hh, &mm);<br />
            int end = hh * 60 + mm;<br />
            Trip trip;<br />
            trip.startTime = start;<br />
            trip.arriveTime = end;<br />
            if (i < na) {<br />
                trip.from = 0;<br />
            }else{<br />
                trip.from = 1;<br />
            }<br />
            trips.push_back(trip);<br />
        }<br />
        <br />
        sort(trips.begin(), trips.end(), sortByMe);<br />
        vector<int> trainsA;<br />
        vector<int> trainsB;</int></int></trip></p>

<p>        int countA = 0, countB = 0;<br />
        <br />
        for (int i = 0; i < na + nb; i++) {<br />
            Trip trip = trips[i];<br />
            if (trip.from == 0) {<br />
                if (trainsA.size() == 0) {<br />
                    countA++;<br />
                }else{<br />
                    bool found = false;<br />
                    vector<int>::iterator iter = trainsA.begin();<br />
                    for (; iter != trainsA.end(); iter++) {<br />
                        if (*iter <= trip.startTime) {<br />
                            trainsA.erase(iter);<br />
                            found = true;<br />
                            break;<br />
                        }<br />
                    }<br />
                    if (found == false) {<br />
                        countA++;<br />
                    }<br />
                }<br />
                trainsB.push_back(trip.arriveTime + t);<br />
            }else{<br />
                if (trainsB.size() == 0) {<br />
                    countB++;<br />
                }else{<br />
                    bool found = false;<br />
                    vector<int>::iterator iter = trainsB.begin();<br />
                    for (; iter != trainsB.end(); iter++) {<br />
                        if (*iter <= trip.startTime) {<br />
                            trainsB.erase(iter);<br />
                            found = true;<br />
                            break;<br />
                        }<br />
                    }<br />
                    if (found == false) {<br />
                        countB++;<br />
                    }<br />
                }<br />
                trainsA.push_back(trip.arriveTime + t);<br />
            }<br />
        }<br />
        <br />
        printf("Case #%d: %d %d\n", c+1, countA, countB);<br />
    }<br />
    <br />
    fclose(stdin);<br />
    fclose(stdout);<br />
    return 0;<br />
}
</int></int></p>

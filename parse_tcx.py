from datetime import datetime
import untangle
import json

def parse_tcx(tcx_file):
    
    parsed_xml = untangle.parse(tcx_file)
    activity = dict()
    laps = []

    for lap in parsed_xml.TrainingCenterDatabase.Activities.Activity.Lap:
        track_points = []
        
        for trackpoint in lap.Track.Trackpoint:
            track_points.append({
                'raw_time' : trackpoint.Time.cdata,
                'parsed_time' : datetime.strptime(trackpoint.Time.cdata, "%Y-%m-%dT%H:%M:%S.%f%z"),
                'altitude_meters' : float(trackpoint.AltitudeMeters.cdata),
                'altitude_gain_loss' : float(trackpoint.AltitudeMeters.cdata)-track_points[-1]['altitude_meters'] if len(track_points) >1 else 0,
                'hr' : int(trackpoint.HeartRateBpm.Value.cdata),
                'speed' : float(trackpoint.Extensions.ns3_TPX.ns3_Speed.cdata),
                'cadence' : float(trackpoint.Extensions.ns3_TPX.ns3_RunCadence.cdata)*2
                }
                )
            
            try:
                track_points[-1]['power'] = float(trackpoint.Extensions.ns3_TPX.ns3_Watts.cdata)
            except:
                track_points[-1]['power'] = 0.0
                if track_points[-1]['speed'] != 0.0:
                    if "notes" in track_points[-1].keys():
                        track_points[-1]['notes'].append("Error power/speed one 0")
                    else:
                        track_points[-1]['notes'] = ["Error power/speed one 0"]
                    

        lap = {
            'notes' :  [x['notes'] for x in track_points if 'notes' in x.keys()] ,
            'distance' : float(lap.DistanceMeters.cdata),
            # 'duration' :  max([x['parsed_time'] for x in track_points]) - min([x['parsed_time'] for x in track_points]),
            # 'start_time' : min([x['parsed_time'] for x in track_points]),
            # 'end_time' : max([x['parsed_time'] for x in track_points]),
            'max_hr' : max( [x['hr'] for x in track_points]),
            'min_hr' : min( [x['hr'] for x in track_points]),
            'avg_hr' : float(sum([x['hr'] for x in track_points])/len(track_points)),
            'max_speed' : max( [x['speed'] for x in track_points] ),
            'min_speed' : min( [x['speed'] for x in track_points] ),
            'avg_speed' : float(sum([x['speed'] for x in track_points])/len(track_points)),
            'max_cadence' : max( [x['cadence'] for x in track_points] ),
            'min_cadance' : min( [x['cadence'] for x in track_points] ),
            'avg_cadence' : float(sum([x['cadence'] for x in track_points])/len(track_points)),
            'max_power' : max( [x['power'] for x in track_points] ),
            'min_power' : min( [x['power'] for x in track_points] ),
            'avg_power' : float(sum([x['power'] for x in track_points])/len(track_points)),
            'track_points' : track_points
                    }
        
        laps.append(lap)
    
    
    
    activity_summary= {
        'distance' : sum([lap['distance'] for lap in laps]),
        'duration' : laps[-1]['track_points'][-1]['parsed_time'] - laps[0]['track_points'][0]['parsed_time'],
        'average_hr' : float(sum([sum([x['hr'] for x in lap['track_points']]) for lap in laps])/sum([len(lap["track_points"]) for lap in laps])),
        'average_speed' : float(sum([sum([x['speed'] for x in lap['track_points']]) for lap in laps])/sum([len(lap["track_points"]) for lap in laps])),
        'average_cadence' : float(sum([sum([x['cadence'] for x in lap['track_points']]) for lap in laps])/sum([len(lap["track_points"]) for lap in laps])),
        
                        }
    
    activity_summary['duration'] = activity_summary['duration'].seconds
    activity['summary'] = activity_summary
    
    activity['laps'] = laps
    
    return activity

def make_activity_json(activity_dict):
    pass

if __name__ == "__main__":
    with  open("activity_17864758309.tcx", "r") as file:
        print(parse_tcx(file)["summary"])


        
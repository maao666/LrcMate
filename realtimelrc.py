# import pylyrics
import logging
# import vlc
#logging.basicConfig(level = logging.DEBUG)

def lrc_interpreter(lrcrawtext):
    lrc_line_list = lrcrawtext.split('\n')
    lrc_converted_list = []
    for individual_line in lrc_line_list:
        # To handle multiple timestamps like [00:01.00][00:04.29]Something
        while True:
            left_bracket_index = individual_line.find('[')
            right_bracket_index = individual_line.find(']')
            if left_bracket_index == -1 or right_bracket_index == -1:
                break
            else:
                # Find minute
                time_stamp = individual_line[left_bracket_index + 1 : right_bracket_index]
                time_colon_index = time_stamp.find(':')
                time_minute = time_stamp[0 : time_colon_index] 
                try:
                    time_minute = int(time_minute)
                except:
                    break
                # Find second
                time_dot_index = time_stamp.find('.')
                time_second = time_stamp[time_colon_index + 1: time_dot_index]
                try:
                    time_second = int(time_second)
                except:
                    break
                # Find millisec
                time_millisec = time_stamp[time_dot_index + 1: right_bracket_index]
                # In case it's in the format of [00:01.00] not [00:01.000]
                if len(time_millisec.strip()) < 3:
                    try:
                        time_millisec = int(time_millisec) * 10**(3 - len(time_millisec.strip()))
                    except:
                        break
                try:
                    time_millisec = int(time_millisec)
                except:
                    break
                logging.debug('Got timestamp {0}:{1}.{2}'.format(time_minute, time_second, time_millisec))
                # Calculate total millisec
                timestamp_in_millisec = time_minute * 60*1000 + time_second * 1000 + time_millisec * 1
                # Append new timestamp to a list
                rightmost_bracket_index = individual_line.rfind(']')
                lrc_converted_list.append((timestamp_in_millisec, individual_line[rightmost_bracket_index +1 : ]))
                logging.debug('Got {}'.format(lrc_converted_list[-1]))
                # Trim current time stamp
                individual_line = individual_line[right_bracket_index +1 :]
        
    return lrc_converted_list


class RTLyrics:
    def _get_millisec(self,elem):
        return elem[0]
    
    def __init__(self, lrctext):
        if not str(type(lrctext)) == "<class 'str'>":
            raise TypeError('lrctext has to be a string containing lyrics')
        self.lrclist = lrc_interpreter(lrctext)
        self.lrclist.sort(key = self._get_millisec)

    def current_lyrics(self, timestamp):
        if not str(type(timestamp)) == "<class 'int'>":
            raise TypeError('Time stamp has to be a number in millisecond. i.e. 81713')
        # TODO: This method has to be replaced by some wise one asap
        if len(self.lrclist) == 0: 
            #In case lrc is empty
            return ''

        for i in range(len(self.lrclist) - 1): 
            if timestamp > self.lrclist[i][0] and timestamp < self.lrclist[i+1][0]:
                # The case we got it!
                lyrics_index = i
                break
            elif timestamp > self.lrclist[i][0] and timestamp > self.lrclist[i+1][0]:
                lyrics_index = -1
                # The case that moves to next item
                continue
            else:
                # Nothing found
                lyrics_index = -1
        if not lyrics_index == -1:
            return self.lrclist[lyrics_index][1]
        else:
            return ''

import requests
import re

def download_m3u(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def process_m3u(m3u_content):
    lines = m3u_content.splitlines()
    channel_dict = {}
    current_channel = None

    for line in lines:
        if line.startswith('#EXTINF'):
            current_channel = line
            match = re.search(r'tvg-name="([^"]+)"', line)
            if match:
                channel_name = match.group(1)
                if channel_name not in channel_dict:
                    channel_dict[channel_name] = {'hevc': None, 'normal': None, 'fps': None}
        elif line.startswith('http') and current_channel:
            if 'HEVC' in current_channel:
                channel_dict[channel_name]['hevc'] = (current_channel, line)
            elif '50 FPS' in current_channel:
                channel_dict[channel_name]['fps'] = (current_channel, line)
            else:
                channel_dict[channel_name]['normal'] = (current_channel, line)
            current_channel = None

    new_m3u_content = "#EXTM3U\n"
    for channels in channel_dict.values():
        if channels['hevc']:
            new_m3u_content += f"{channels['hevc'][0]}\n{channels['hevc'][1]}\n"
        elif channels['normal']:
            new_m3u_content += f"{channels['normal'][0]}\n{channels['normal'][1]}\n"
        elif channels['fps']:
            new_m3u_content += f"{channels['fps'][0]}\n{channels['fps'][1]}\n"

    return new_m3u_content

def save_m3u(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/itv_proxy.m3u"
    m3u_content = download_m3u(url)
    new_m3u_content = process_m3u(m3u_content)
    save_m3u(new_m3u_content, 'processed_playlist.m3u')
    print("Processed M3U playlist saved as 'processed_playlist.m3u'")

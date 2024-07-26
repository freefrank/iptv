import requests

def download_m3u(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def process_m3u(content):
    channels = {}
    output_lines = []
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('#EXTINF'):
            tvg_id = get_tvg_id(line)
            quality = get_quality(line)
            
            if tvg_id not in channels:
                channels[tvg_id] = (line, lines[i + 1].strip(), quality)
            else:
                if quality_priority(quality) > quality_priority(channels[tvg_id][2]):
                    channels[tvg_id] = (line, lines[i + 1].strip(), quality)
            i += 1
        else:
            output_lines.append(line)
        i += 1

    for info in channels.values():
        output_lines.append(info[0])
        output_lines.append(info[1])
        
    return '\n'.join(output_lines)

def get_tvg_id(extinf_line):
    start = extinf_line.find('tvg-id="') + len('tvg-id="')
    end = extinf_line.find('"', start)
    return extinf_line[start:end]

def get_quality(extinf_line):
    if 'HEVC' in extinf_line:
        return 'HEVC'
    elif '50 FPS' in extinf_line:
        return '50 FPS'
    else:
        return 'NORMAL'

def quality_priority(quality):
    if quality == 'HEVC':
        return 3
    elif quality == 'NORMAL':
        return 2
    elif quality == '50 FPS':
        return 1
    else:
        return 0

def save_m3u(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

def main():
    url = 'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/itv_proxy.m3u'
    content = download_m3u(url)
    processed_content = process_m3u(content)
    save_m3u(processed_content, 'processed_itv_proxy.m3u')

if __name__ == '__main__':
    main()

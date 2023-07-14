"""
    The script generates an image graph.png in the program directory, 
    as well as graph-<timestamp>.png in the **images** folder 
    (folder **pcap** contains example pcap files). For Windows hosts.
"""


import os
import subprocess
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

root = 'D:\\05\\PcapGraphBuilder\\'


def file_loader(filename="tshark.csv"):
    """Open .csv file and count IP pairs

    Args:
        filename (optional): Hardcoded string value. Defaults to "tshark.csv".

    Returns:
        ip_dict: Dictionaty with IP addresses pairs
    """
    try:
        ip_list = []
        with open(root + filename, "r") as file:
            for line in file.readlines():
                ip_list.append(line[0:-1].replace('"', '').split(','))
    except BaseException:
        print("File not found...")
    ip_list = ['-'.join(sorted(x)) for x in ip_list]
    ip_dict = {x: 0 for x in ip_list}
    for x in ip_list:
        if x in ip_dict.keys():
            ip_dict[x] += 1
    return ip_dict


def make_graph_edges(ip_dict):
    """Function for constructing edges

    Args:
        ip_dict: Dictionaty with IP addresses pairs
    """
    for k, v in ip_dict.items():
        edge_a = k.split('-')[0]
        edge_b = k.split('-')[1]
        weight_ab = v
        G.add_edge(str(edge_b), str(edge_a), weight=weight_ab, size=11300)
    return 0


def draw_graph():
    """Function for drawing the constructed graph"""
    pos = nx.circular_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx(G,
                     pos, with_labels=True,
                     font_size=12,
                     node_size=7000,
                     node_color='black',
                     font_color='white',
                     edge_color='blue',
                     linewidths=4.0,
                     width=2.0)
    nx.draw_networkx_edge_labels(G,
                                 pos,
                                 edge_labels=edge_labels,
                                 font_color='black',
                                 font_size=12,
                                 bbox=dict(
                                     facecolor='white',
                                     edgecolor='blue',
                                     boxstyle='circle',
                                     lw=1))
    plt.gcf().set_size_inches(17, 17)
    plt.axis('off')
    plt.savefig(
        root + "images/graph-{}.png".format(datetime.today().timestamp()))
    plt.savefig(root + "graph.png")
    return 0


def shark_me(filename):
    """Translate .pcap to .сsv"""
    tsharkCall = [f"C:\\Program Files\\Wireshark\\tshark.exe",
                  "-r",
                  root + filename,
                  "-Tfields",
                  "-E",
                  "separator=,",
                  "-E",
                  "header=n",
                  "-E",
                  "quote=d",
                  "-e",
                  "ip.src",
                  "-e",
                  "ip.dst",
                  "-Y",
                  "ip.addr ne 0.0.0.0"]
    tshark_out = open("tshark.csv", "wb")
    tshark_proc = subprocess.check_call(
        tsharkCall, stdout=tshark_out, shell=True)
    tshark_out.close()
    return 0


def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    """Function to scale output Image"""
    original_image = Image.open(input_image_path)
    w, h = original_image.size

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        raise RuntimeError('Width or height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size


G = nx.MultiDiGraph()
shark_me('pcap\\5.pcapng')
file_loader()
make_graph_edges(file_loader())
draw_graph()
scale_image(
    input_image_path='graph.png',
    output_image_path='graph.png',
    width=12000)
os.remove(root + "tshark.csv")

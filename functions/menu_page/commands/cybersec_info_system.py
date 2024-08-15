import streamlit as st
import platform
import subprocess


def run_command(command):
    """
    Runs a command in a new terminal.
    """
    if platform.system() == 'Windows':
        subprocess.Popen(['start', 'cmd', '/k', command], shell=True)
    elif platform.system() == 'Linux':
        subprocess.Popen(['gnome-terminal', '-e', command])
    elif platform.system() == 'Darwin':
        subprocess.Popen(['open', '-a', 'Terminal.app', command])

class InfoCommands:
    def __init__(self, listen):
        self.listen = listen

    def ip_config(self):
        """
        Displays the computer's IP configuration.
        """
        ip_keywords = ['lumen quel est mon ip', 'lumen quelle est mon ip', 'lumen mon ip', 'lumen my ip',
                       'lumen what is my ip', 'lumen what\'s my ip']
        if any(keyword in self.listen for keyword in ip_keywords):
            if platform.system() == 'Windows':
                run_command('ipconfig')
            elif platform.system() == 'Linux':
                run_command('ifconfig')
            elif platform.system() == 'Darwin':
                run_command('ifconfig')

    def system_info(self):
        """
        Displays computer system information.
        """
        sys_info_keywords = ['lumen informations sur mon système', 'lumen information sur mon système',
                    'lumen informations système', 'lumen information système',
                    'lumen informations of my system', 'lumen information of my system',
                    'lumen informations system', 'lumen information system']
        if any(keyword in self.listen for keyword in sys_info_keywords):
            if platform.system() == 'Windows':
                run_command('systeminfo')
            elif platform.system() == 'Linux':
                run_command('uname -a')
            elif platform.system() == 'Darwin':
                run_command('system_profiler SPSoftwareDataType')

    def net_info(self):
        """
        Displays netstat network information.
        """
        netstat_info_keywords = ['lumen informations sur le netstat', 'lumen informations netstat', 
                            'lumen informations of my netstat', 'lumen informations netstat',
                            'lumen information sur le netstat', 'lumen information netstat', 
                            'lumen information of my netstat', 'lumen information netstat']
        if any(keyword in self.listen for keyword in netstat_info_keywords):
            if platform.system() == 'Windows':
                run_command('netstat -a')
            elif platform.system() == 'Linux':
                run_command('netstat -a')
            elif platform.system() == 'Darwin':
                run_command('netstat -a')

    def arp_info(self):
        """
        Displays arp network information.
        """
        arp_info_keywords = ['lumen informations sur l\'arp', 'lumen informations arp', 
                            'lumen informations of my arp', 'lumen informations arp',
                            'lumen information sur l\'arp', 'lumen information arp', 
                            'lumen information of my arp', 'lumen information arp']
        if any(keyword in self.listen for keyword in arp_info_keywords):
            if platform.system() == 'Windows':
                run_command('arp -a')
            elif platform.system() == 'Linux':
                run_command('arp -a')
            elif platform.system() == 'Darwin':
                run_command('arp -a')

    def route_info(self):
        """
        Displays route information.
        """
        route_info_keywords = ['lumen informations route', 'lumen informations routes',
                               'lumen information route', 'lumen information routes']
        if any(keyword in self.listen for keyword in route_info_keywords):
            if platform.system() == 'Windows':
                run_command('route print')
            elif platform.system() == 'Linux' or platform.system() == 'Darwin':
                run_command('netstat -r')
            else:
                st.sidebar.error("The route print command is not available on this OS.")

    def schtasks_info(self):
        """
        Displays scheduled tasks information.
        """
        tasks_info_keywords = ['lumen informations task', 'lumen informations tasks',
                               'lumen information task', 'lumen information tasks']
        if any(keyword in self.listen for keyword in tasks_info_keywords):
            if platform.system() == 'Windows':
                run_command('schtasks /query')
            else:
                st.sidebar.error("The schtasks /query command is not available on this OS.")

    def driver_info(self):
        """
        Displays driver information.
        """
        driver_info_keywords = ['lumen informations driver', 'lumen informations drivers', 
                                'lumen driver informations', 'lumen drivers informations',
                                'lumen information driver', 'lumen information drivers', 
                                'lumen driver information', 'lumen drivers information']
        if any(keyword in self.listen for keyword in driver_info_keywords):
            if platform.system() == 'Windows':
                run_command('driverquery')
            else:
                st.sidebar.error("The driverquery command is not available on this operating system.")

    def msinfo32_info(self):
        """
        Displays msinfo32 information.
        """
        msinfo_info_keywords = ['lumen informations ms', 'lumen informations machine système', 
                                'lumen informations système machine', 'lumen informations machine system',
                                'lumen information ms', 'lumen information machine système', 
                                'lumen information système machine', 'lumen information machine system']
        if any(keyword in self.listen for keyword in msinfo_info_keywords):
            if platform.system() == 'Windows':
                run_command('msinfo32')
            else:
                st.sidebar.error("The msinfo32 command is not available on this operating system.")
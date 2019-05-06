using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Xml;
using System.IO;
using System.Net;

namespace HttpClient
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        private System.Threading.Thread upload_T;
        private static string url = "";
        private string folder = "";
        private bool delete = false;
        private void Form1_Load(object sender, EventArgs e)
        {
            log("app start.");
            loadoption();
            txtBox_url.Text = url;
            txtBoxFolder.Text = folder;
            checkBoxdelete.Checked = delete;

            timer.Enabled = true;
        }
        private void Form1_Shown(object sender, EventArgs e)
        {
            //this.Hide();
        }
        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {

        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            saveoption();
            log("app close.");
            if(upload_T!=null)
            {
                ran = false;
                upload_T.Abort();
                upload_T = null;
            }
            timer.Enabled = false;
        }
        //写入日志
        private void log(string str)
        {
            string path = "l" + DateTime.Now.ToString("yyyyMM") + ".txt";
            string contents = DateTime.Now.ToString("yyyy/MM/dd HH:mm:ss") + "\t"+str+"\r\n";
            File.AppendAllText(path, contents);
        }
        //加在配置
        private void loadoption()
        {
            XmlDocument xmldoc = new XmlDocument();
            if(System.IO.File.Exists("options.xml"))
            {
                xmldoc.Load("options.xml");
                for (int i = 0; i < xmldoc.ChildNodes.Count; i++)
                {
                    if (xmldoc.ChildNodes[i].Name == "options")
                    {
                        for (int j = 0; j < xmldoc.ChildNodes[i].ChildNodes.Count; j++)
                        {
                            switch (xmldoc.ChildNodes[i].ChildNodes[j].Name)
                            {
                                case "url":
                                    url = xmldoc.ChildNodes[i].ChildNodes[j].InnerText;
                                    break;
                                case "folder":
                                    folder = xmldoc.ChildNodes[i].ChildNodes[j].InnerText;
                                    break;
                                case "delete":
                                    delete = bool.Parse(xmldoc.ChildNodes[i].ChildNodes[j].InnerText);
                                    break;
                                default:
                                    break;
                            }
                        }
                    }
                }
            }
        }
        //保存配置
        private void saveoption()
        {
            XmlDocument xmldoc = new XmlDocument();
            if (File.Exists("options.xml"))
            {
                xmldoc.Load("options.xml");
                for (int i = 0; i < xmldoc.ChildNodes.Count; i++)
                {
                    if (xmldoc.ChildNodes[i].Name == "options")
                    {
                        for (int j = 0; j < xmldoc.ChildNodes[i].ChildNodes.Count; j++)
                        {
                            switch (xmldoc.ChildNodes[i].ChildNodes[j].Name)
                            {
                                case "url":
                                    xmldoc.ChildNodes[i].ChildNodes[j].InnerText = url;
                                    break;
                                case "folder":
                                    xmldoc.ChildNodes[i].ChildNodes[j].InnerText = folder;
                                    break;
                                case "delete":
                                    xmldoc.ChildNodes[i].ChildNodes[j].InnerText = delete.ToString();
                                    break;
                                default:
                                    break;
                            }
                        }
                    }
                }
                xmldoc.Save("options.xml");
            }
            else
            {

            }
        }

        private void btnFolder_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog())
            {
                folderBrowserDialog.ShowNewFolderButton = false;
                DialogResult dr = folderBrowserDialog.ShowDialog();
                if (dr == DialogResult.OK)
                {
                    if (folderBrowserDialog.SelectedPath.ToString() != "")
                    {
                        txtBoxFolder.Text = folderBrowserDialog.SelectedPath.ToString();
                        folder = txtBoxFolder.Text;
                    }
                    folderBrowserDialog.Dispose();
                }
                if (dr == DialogResult.Cancel)
                {

                }
            }
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            if (ran)
            {
                ran=false;
                btnStart.Text = "启动";
                btnStart.BackColor = Color.FromKnownColor(KnownColor.Control);
                upload_T.Abort();
                upload_T = null;
            }
            else
            {
                ran = true;
                btnStart.Text = "停止";
                btnStart.BackColor = Color.Green;
                upload_T = new System.Threading.Thread(() => upload(ref ran));
                upload_T.Start();
            }
        }

        private void Query(DirectoryInfo[] dirsInfo)
        {
            //最后一次写入的文件夹不上传
            for (int i = 0; i < dirsInfo.Length - 1; i++)
            {
                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
                request.Method = "POST";
                var bdy = "---------------------------" + DateTime.Now.Ticks.ToString("x", System.Globalization.NumberFormatInfo.InvariantInfo);
                request.ContentType = "multipart/form-data; boundary=" + bdy;
                bdy = "--" + bdy;
                using (var rr = request.GetRequestStream())
                {
                    //Write POST variables
                    byte[] postbuff = Encoding.ASCII.GetBytes(bdy + "\r\n");
                    rr.Write(postbuff, 0, postbuff.Length);
                    postbuff = Encoding.ASCII.GetBytes(string.Format("Content-Disposition: form-data; name=\"{0}\"{1}{1}", "num_files", "\r\n"));
                    rr.Write(postbuff, 0, postbuff.Length);
                    postbuff = Encoding.UTF8.GetBytes(dirsInfo[i].GetFiles().Length + "\r\n");
                    rr.Write(postbuff, 0, postbuff.Length);
                    //Write POST files
                    FileInfo[] fileInfos = dirsInfo[i].GetFiles();
                    Stream[] stream = new MemoryStream[fileInfos.Length];
                    for (int j = 0; j < fileInfos.Length; j++)
                    {
                        FileStream fileStream = new FileStream(fileInfos[j].FullName, FileMode.Open, FileAccess.Read);
                        byte[] buff = new byte[fileStream.Length];
                        while ((fileStream.Read(buff, 0, buff.Length)) != 0)
                        {
                            stream[j] = new MemoryStream();
                            stream[j].Write(buff, 0, buff.Length);
                        }
                        byte[] filebuff = Encoding.ASCII.GetBytes(bdy + "\r\n");
                        rr.Write(filebuff, 0, filebuff.Length);
                        filebuff = Encoding.UTF8.GetBytes(string.Format("Content-Disposition: form-data; name=\"{0}\"; filename=\"{1}\"{2}", j, fileInfos[j].Name, "\r\n"));
                        rr.Write(filebuff, 0, filebuff.Length);
                        filebuff = Encoding.ASCII.GetBytes(string.Format("Content-Type: {0}{1}{1}", "image/jpeg", "\r\n"));
                        rr.Write(filebuff, 0, filebuff.Length);
                        stream[j].Position = 0;
                        byte[] tempBuffer = new byte[stream[j].Length];
                        stream[j].Read(tempBuffer, 0, tempBuffer.Length);
                        rr.Write(tempBuffer, 0, tempBuffer.Length);
                        filebuff = Encoding.ASCII.GetBytes("\r\n");
                        rr.Write(filebuff, 0, filebuff.Length);
                        fileStream.Close();
                    }
                    byte[] bdybuff = Encoding.ASCII.GetBytes(bdy + "--");
                    rr.Write(bdybuff, 0, bdybuff.Length);
                    //Close and release the resource
                    rr.Close();
                }
                // Get the response
                WebResponse response = request.GetResponse();
                // Display the status.
                Console.WriteLine(((HttpWebResponse)response).StatusDescription);
                // Get the stream containing content returned by the server.
                Stream dataStream = response.GetResponseStream();
                // Open the stream using a StreamReader for easy access.
                StreamReader reader = new StreamReader(dataStream);
                // Read the content.
                string responseFromServer = reader.ReadToEnd();
                //MessageBox.Show(responseFromServer);
                if (responseFromServer == "1111")
                {
                    dirsInfo[i].Delete(true);
                }
                // Clean up the streams and the response.
                reader.Close();
                response.Close();
                //Stream requeststream = null;
                //try
                //{
                //    requeststream = request.GetRequestStream();
                //}
                //catch (Exception ex)
                //{
                //    log(ex.ToString());
                //}
            }
        }

        private bool ran = false;
        private void upload(ref bool ran)
        {
           
            while (ran)
            {
                DirectoryInfo dirs = new DirectoryInfo(folder);//"根目录"
                DirectoryInfo[] dirsInfo=dirs.GetDirectories();//"根目录"下文件夹
                //根据文件夹最后一次写入时间排序
                for(int i=0;i<dirsInfo.Length-1;i++)
                {
                    if(dirsInfo[i].LastWriteTime > dirsInfo[i+1].LastWriteTime)
                    {
                        DirectoryInfo dirstemp = dirsInfo[i];
                        dirsInfo[i] = dirsInfo[i + 1];
                        dirsInfo[i + 1] = dirstemp;
                    }
                }
                Query(dirsInfo);
            }  
        }

        //最小化，显示系统托盘
        private void Form1_SizeChanged(object sender, EventArgs e)
        {

        }

        private void checkBoxdelete_CheckedChanged(object sender, EventArgs e)
        {
            delete = checkBoxdelete.Checked;
        }

        private void notifyIcon_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            if (this.Visible)
            {
                this.Hide();
                //MessageBox.Show("已经显示");
            }
            else
            {
                this.Show();
                this.WindowState = FormWindowState.Normal;
            }
        }

        private void timer_Tick(object sender, EventArgs e)
        {
            toolStripStatusLabel.Text = DateTime.Now.ToString("yyyy/MM/dd HH:mm:ss");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.Icon= ((System.Drawing.Icon)(resources.GetObject("ng.Icon"))); 
        }
    }
}

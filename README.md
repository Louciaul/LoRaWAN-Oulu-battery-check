# LoWaRAN-Oulu-battery-check

This repository allows the user to detect which device is failing in Oulu's university LoWaRAN network

## Prerequisite

```bash
pip install influxdb
```

## Run the code

This code connects to Oulu's LoWaRAN network influxDB endpoint

To run the code use:

```bash
python main.py
```

Then enter your credentials

As the database start to be huge, it may take 20 minutes to run entirely

## TO READ

This programm can be improved by making change in the precision of the battery level. At this point I had no idea at which point the battery will make the device failed, from arbitrary decision when seeing all the data, most devices that don't fail are above 3.6 V. A lot of devices fail when under 2.5 V. 

I added global variable, you can then change in [main.py](main.py):
- the time guard for last data published
- the minimum battery level to trigger a suspicious device

## Results

You can see the result in the [SUSPECT.txt](suspect.txt) file

You will find:

- A highly suspected list of devices: these devices failed to publish data since 14 days (default) and have a low level of battery (< 2.5 V by default)

- A low suspected list of devices: these devices failed to publish data since 14 days (default) but have a normal level of battery

## How to locate the device

go on https://smartcampus.oulu.fi/manage/list

then enter the id of the device without the "-"

example:
- ab-cd-ef-gh-ij-kl-mn-op -> abcdefghijklmnop

## License

This project is under the GNU GENERAL PUBLIC LICENSE-3.0 new or revised license. Please read the [LICENSE](LICENSE) file.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

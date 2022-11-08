# InControl2ConfigDownloader

This is a Python3 script that willd download the most recent configurations for every device in a Peplink InControl2 organization. It will not check if a configuration has already been saved, but it will just download the most current config again.

Using a .env file, please add `incontrol_client_id` and `incontrol_client_secret` from making a client at [https://incontrol2.peplink.com/r/user/edit](https://incontrol2.peplink.com/r/user).

TODO:

- Add token refresh instead of just getting a new token
- Error checking for each request by using response codes

## As Is Software

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE OPEN GROUP BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

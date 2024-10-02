# LDNSpOwer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/downloads/)

A powerful, user-friendly DNS management tool that allows you to easily change your system's DNS settings and test DNS performance for specific domains. Built with modern Python practices and a beautiful CLI interface.

![LDNSpOwer Demo](https://via.placeholder.com/600x400.png?text=LDNSpOwer+Demo)

## ✨ Features

- 🎨 Beautiful CLI interface using Rich
- 🚀 Lightning-fast DNS performance testing
- ⭐ Smart ranking system for DNS servers
- 🔒 Secure handling of system commands (no manual sudo required)
- 🌍 Support for both IPv4 and IPv6
- 📊 Visual comparison of DNS performance
- 🔄 Automatic network connection handling

## 🚀 Installation

```bash
# Using pip
pip install ldnspower

# Or clone and install locally
git clone https://github.com/pakrohk/ldnspower.git
cd ldnspower
pip install -e .
```

## 📋 Requirements

- Python 3.7 or higher
- NetworkManager
- Linux-based operating system

## 🎮 Usage

Basic usage:
```bash
ldnspower
```

Test DNS speeds for a specific domain:
```bash
ldnspower --domain example.com
```

### Available DNS Servers

| Provider    | IPv4 Primary    | IPv4 Secondary  | Ranking |
|-------------|-----------------|-----------------|---------|
| Google      | 8.8.8.8         | 8.8.4.4         | ⭐⭐⭐⭐⭐ |
| Cloudflare  | 1.1.1.1         | 1.0.0.1         | ⭐⭐⭐⭐⭐ |
| OpenDNS     | 208.67.222.222  | 208.67.220.220  | ⭐⭐⭐⭐  |
| Comodo      | 8.26.56.26      | 8.20.247.20     | ⭐⭐⭐   |
| Shecan      | 178.22.122.100  | 185.51.200.2    | ⭐⭐⭐   |
| ElTeam Gaming | 78.157.42.100 | 78.157.42.101   | ⭐⭐     |
| Begzar      | 185.55.226.26   | 185.55.225.25   | ⭐⭐     |
| 403         | 10.202.10.202   | 10.202.10.102   | ⭐      |

## 🛠️ Development

Want to contribute? Great! Here's how you can help:

1. Fork the repo
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -am 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Running Tests

```bash
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Pakrohk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Special thanks to Claude AI for the excellent guidance and suggestions
- Inspired by the original DnsChanger.sh script
- Thanks to all contributors who have helped shape this project

## 📬 Contact

Pakrohk - [@pakrohk](https://github.com/pakrohk)

Project Link: [https://github.com/pakrohk/ldnspower](https://github.com/pakrohk/ldnspower)

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

## 🗺️ Roadmap

- [ ] Add support for more operating systems
- [ ] Create a GUI version
- [ ] Add automatic DNS suggestion based on location
- [ ] Implement DNS-over-HTTPS support
- [ ] Add more DNS providers

See the [open issues](https://github.com/pakrohk/ldnspower/issues) for a full list of proposed features (and known issues).

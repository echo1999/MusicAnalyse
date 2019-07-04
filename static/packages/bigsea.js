// 定义 log
const log = console.log.bind(console, '🐸')
// bigsea.js
class SEA {
	constructor(select) {
		if (typeof select == 'string') {
			this.arr = Array.from(document.querySelectorAll(select))
		} else if (select && select.addEventListener) {
			this.arr = [select]
		} else {
			this.arr = []
		}
		this.dom = this.arr[0]
	}
	// 观察者
	ob(options, callback) {
		// www.cnblogs.com/jscode/p/3600060.html
		let _callback = e => {
			callback.bind(this.dom)(e[0])
		}
		let listen = new MutationObserver(_callback)
		for (let dom of this.arr) {
			listen.observe(dom, options)
		}
	}

	// 事件 (绑定/委托)
	on(names, select, callback, one) {
		let off = function (e, arr) {
			if (Array.isArray(e.sea_event)) {
				e.sea_event.push(arr)
			} else {
				e.sea_event = [arr]
			}
		}
		// 多个事件
		for (let name of names.split(' ')) {
			// 参数转换
			if (callback === undefined) {
				callback = select
				// 绑定
				for (let e of this.arr) {
					let _callback = function (event) {
						callback.call(e, event)
						if (one === true) {
							e.removeEventListener(name, _callback)
						}
					}
					e.addEventListener(name, _callback, false)
					off(e, [name, select, _callback])
				}
			} else {
				// 委托
				for (let e of this.arr) {
					let _callback = function (event) {
						let parent = Sea(event.target).parent(select).dom
						this.querySelectorAll(select).forEach(function (dom, index) {
							if (dom.isSameNode(parent)) {
								// callback.bind(dom)(event, index)
								callback.call(dom, event, index)
								if (one === true) {
									e.removeEventListener(name, _callback)
								}
							}
						})
					}
					if (['blur', 'focus'].includes(name)) {
						e.addEventListener(name, _callback, true)
					} else {
						e.addEventListener(name, _callback, false)
					}
					off(e, [name, select, _callback])
				}
			}
		}
	}
	// 一次性事件 (绑定/委托)
	one(name, select, callback) {
		this.on(name, select, callback, true)
	}
	// 移除事件
	off() {
		for (let e of this.arr) {
			if (Array.isArray(e.sea_event)) {
				for (let arr of e.sea_event) {
					let [name, select, callback] = arr
					e.removeEventListener(name, callback)
				}
				e.sea_event = undefined
			}
		}
		return this
	}
	// 触发自定义事件
	iEvent(name, obj, bubble) {
		let e = new Event(name, {
			bubbles: bubble || true,
		})
		e.data = obj || {}
		for (let dom of this.arr) {
			dom.dispatchEvent(e)
		}
	}

	// 样式
	css(obj, val) {
		let set = (k, v) => {
			for (let e of this.arr) {
				e.style[k] = String(v)
			}
		}
		if (typeof obj === 'string') {
			if (val === undefined) {
				return window.getComputedStyle(this.dom)[obj]
			} else {
				set(obj, val)
			}
		} else {
			for (let key in obj) {
				set(key, obj[key])
			}
		}
		return this
	}
	// 显示
	show(str) {
		for (let e of this.arr) {
			e.style.display = str || e.sea_display || 'flex'
		}
		return this
	}
	// 隐藏
	hide() {
		for (let e of this.arr) {
			let display = window.getComputedStyle(e).display
			if (display !== 'none') {
				e.sea_display = display
			}
			e.style.display = 'none'
		}
		return this
	}

	// 查找子元素
	find(select) {
		let sea = Sea()
		let arr = []
		if (this.dom) {
			for (let e of this.arr) {
				Array.from(e.querySelectorAll(select)).forEach(e => {
					arr.push(e)
				})
			}
			sea.arr = arr
			sea.dom = arr[0]
		}
		return sea
	}
	// 查找父元素
	parent(select) {
		let sea = Sea()
		let arr = []
		if (this.dom) {
			if (select) {
				arr.push(this.dom.closest(select))
			} else {
				arr.push(this.dom.parentElement)
			}
			sea.arr = arr
			sea.dom = arr[0]
		}
		return sea
	}
	// 查找上一个元素
	prev() {
		if (this.dom) {
			return Sea(this.dom.previousSibling)
		}
	}
	// 查找下一个元素
	next() {
		if (this.dom) {
			return Sea(this.dom.nextSibling)
		}
	}
	// 子元素
	child() {
		let sea = Sea()
		let arr = []
		for (let e of this.dom.childNodes) {
			arr.push(e)
		}
		sea.arr = arr
		sea.dom = arr[0]
		return sea
	}
	// 选择
	eq(i) {
		let sea = Sea()
		if (typeof i === 'number') {
			let end = i + 1 === 0 ? undefined : i + 1
			let arr = this.arr.slice(i, end)
			sea.arr = arr
			sea.dom = arr[0]
		}
		return sea
	}
	// 循环
	each(callback) {
		// 在 callback 中 return = null 相当于 break
		for (let i = 0; i < this.arr.length; i++) {
			let e = new SEA(this.arr[i])
			// callback.bind(this.dom)(e, i)
			if (callback.call(this.arr[i], e, i) === null) {
				break
			}
		}
	}

	// 添加类
	addClass(str) {
		for (let e of this.arr) {
			for (let cls of str.split(' ')) {
				e.classList.add(cls)
			}
		}
		return this
	}
	// 删除类
	removeClass(str) {
		for (let e of this.arr) {
			for (let cls of str.split(' ')) {
				e.classList.remove(cls)
			}
		}
		return this
	}
	// 判断包含类
	hasClass(str) {
		return this.dom.classList.contains(str)
	}
	// 开关类
	toggleClass(str) {
		for (let e of this.arr) {
			return e.classList.toggle(str)
		}
	}

	// 获取或设置 文本
	text(text) {
		if (typeof text == 'string') {
			for (let e of this.arr) {
				e.innerText = text
			}
		} else {
			if (this.dom) {
				return this.dom.innerText
			}
		}
	}
	// 获取或设置 HTML
	html(html) {
		if (typeof html == 'string') {
			for (let e of this.arr) {
				e.innerHTML = html
			}
		} else {
			if (this.dom) {
				return this.dom.innerHTML
			}
		}
	}
	// value
	val(str) {
		if (this.dom) {
			if (str !== undefined) {
				for (let e of this.arr) {
					e.value = str
				}
				return this
			} else {
				return this.dom.value
			}
		} else {
			return ''
		}
	}
	// dataset
	data(key, val) {
		if (this.dom) {
			if (val !== undefined) {
				for (let e of this.arr) {
					e.dataset[key] = val
				}
			} else {
				return this.dom.dataset[key]
			}
		}
	}

	// 元素内添加
	append(html, where) {
		let s = where || 'beforeend'
		for (let e of this.arr) {
			e.insertAdjacentHTML(s, html)
		}
		return this
	}
	appendChild(dom) {
		for (let e of this.arr) {
			e.appendChild(dom)
		}
		return this
	}
	// 首部 添加
	prepend(html) {
		return this.append(html, 'afterbegin')
	}
	// 之前 添加 现有元素外
	before(html) {
		return this.append(html, 'beforebegin')
	}
	// 元素外添加
	after(html) {
		return this.append(html, 'afterend')
	}
	// 删除
	remove() {
		for (let e of this.arr) {
			e.remove()
		}
	}
	// 获取或设置属性
	attr(key, val) {
		if (this.dom) {
			if (typeof val === 'string') {
				for (let e of this.arr) {
					e.setAttribute(key, val)
				}
			} else {
				return this.dom.getAttribute(key)
			}
		}
	}
	// 删除属性
	removeAttr(key) {
		for (let e of this.arr) {
			e.removeAttribute(key)
		}
		return this
	}
	// 开关属性
	toggleAttr(key, val) {
		if (this.dom) {
			if (this.attr(key) === null) {
				this.attr(key, val || '')
			} else {
				this.removeAttr(key)
			}
		}
	}

	// 点击
	click() {
		this.dom.click()
		return this
	}
	// 获得焦点
	focus() {
		this.dom.focus()
		return this
	}
	// 失去焦点
	blur() {
		this.dom.blur()
		return this
	}
	// 全选
	select() {
		this.dom.select()
		return this
	}
}
// Sea
const Sea = function (select) {
	return new SEA(select)
}
// 静态方法
Sea.static = {
	// 浮点数运算
	float(n) {
		return parseFloat(n.toFixed(10))
	},
	// 测试
	ensure(bool, message) {
		if (!bool) {
			log('测试失败:', message)
		}
	},
	// 循环 n 次后断点
	cut(n) {
		if (Sea.cut.count) {
			Sea.cut.count--
			if (Sea.cut.count == 1) {
				delete Sea.cut.count
				throw `断点：${n}次`
			}
		} else {
			if (n > 1) {
				Sea.cut.count = n
			} else {
				throw `断点`
			}
		}
	},
	// 返回 a-b 的随机数
	random(a, b) {
		return parseInt(Math.random() * (b - a) + a)
	},
	// 正则 特殊字符转义
	re(s, flag) {
		return new RegExp(s.replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$&'), flag || 'g')
	},
	// json 解析
	json(s) {
		try {
			return JSON.parse(s)
		} catch (err) {
			return s
		}
	},
	// 返回数据类型
	type(obj) {
		return Object.prototype.toString
			.call(obj)
			.slice(8, -1)
			.toLowerCase()
	},
	// url 解析
	parseUrl(url) {
		let obj = {}
		let arr = []
		// protocol
		arr = url.split('://')
		obj.protocol = arr[1] ? arr[0] : ''
		url = arr[1] || arr[0]
		// host
		arr = url.split('/')
		obj.host = arr[0]
		url = arr.slice(1).join('/')
		// hash
		arr = url.split('#')
		obj.hash = arr[1] || ''
		url = arr[0]
		// query
		arr = url.split('?')
		obj.query = Sea.query(arr[1])
		url = arr[0]
		// path
		obj.path = '/' + url
		// origin
		obj.origin = ''
		if (obj.protocol && obj.host) {
			obj.origin = obj.protocol + '://' + obj.host
		}
		// href
		obj.href = obj.origin + obj.path
		return obj
	},
	// Ajax
	Ajax(request) {
		const req = {
			method: (request.method || 'GET').toUpperCase(),
			url: request.url || '',
			data: request.data || {},
			query: request.query || {},
			header: request.header || {},
			callback: request.callback,
			cors: request.cors || '',
			hash: request.hash || '',
			timeout: request.timeout,
		}
		// host
		if (!req.url.startsWith('http')) {
			// 默认域名
			req.url = (this.Ajax.HOST || '') + req.url
		}
		// url 解析
		const url = Sea.parseUrl(req.url)
		req.url = url.path
		// query 请求
		let query = Object.assign(url.query, req.query)
		if (req.method === 'GET') {
			query = Object.assign(query, req.data)
		}
		req.url += Sea.query(query)
		// hash 锚点
		const hash = req.hash || url.hash
		if (hash) {
			req.url += '#' + hash
		}
		// cors 跨域
		if (req.cors) {
			req.header.cors = url.origin
			req.url = req.cors + req.url
		} else {
			req.url = url.origin + req.url
		}
		// promise
		return new Promise(function (success, fail) {
			const r = new XMLHttpRequest()
			// 设置超时
			if (req.timeout) {
				r.timeout = req.timeout
			}
			r.open(req.method, req.url, true)
			for (const key in req.header) {
				r.setRequestHeader(key, req.header[key])
			}
			r.onreadystatechange = function () {
				if (r.readyState === 4) {
					const res = Sea.json(r.response)
					// 回调函数
					if (typeof req.callback === 'function') {
						req.callback(res)
					}
					// Promise 成功
					success(res)
				}
			}
			r.onerror = function (err) {
				fail(err)
			}
			if (req.method === 'GET') {
				r.send()
			} else {
				// POST
				if (typeof req.data === 'string') {
					r.send(req.data)
				} else {
					// 默认 json
					r.send(JSON.stringify(req.data))
				}
			}
		})
	},
	// 生成样式 String
	css(css, obj) {
		// Sea.css('top:hover', {'display':'block', 'cursor':'zoom-in'})
		let s = ''
		for (let key in obj) {
			let val = obj[key]
			s += `${key}:${val};`
		}
		if (css) {
			s = `${css}{${s}}`
		}
		return s
	},
	// 生成 query
	query(obj) {
		if (typeof obj === 'string') {
			let result = {}
			let start = obj.indexOf('?')
			let end = obj.indexOf('#')
			if (start === -1) {
				start = 0
			} else {
				start += 1
			}
			if (end === -1) {
				end = obj.length
			}
			obj = obj.slice(start, end)
			if (obj) {
				for (let e of obj.split('&')) {
					let arr = e.split('=')
					result[arr[0]] = arr[1] || ''
				}
			}
			return result
		} else {
			let arr = []
			for (let key in obj) {
				let val = obj[key]
				arr.push([key, val].join('='))
			}
			let s = ''
			if (arr.length) {
				s = '?' + arr.join('&')
			}
			return s
		}
	},
	// 检查 Object
	has(obj, path) {
		path = path.replace(/\[(.+)\]\./, '.$1.')
		if (obj && path) {
			const arr = path.split('.')
			for (const k of arr) {
				if (typeof obj === 'object' && k in obj) {
					obj = obj[k]
				} else {
					return false
				}
			}
			return Boolean(obj)
		}
	},
	// 本地存储
	localStorage(key, val) {
		if (val === undefined) {
			return Sea.json(window.localStorage.getItem(key))
		} else {
			if (val === '') {
				window.localStorage.removeItem(key)
			} else {
				window.localStorage.setItem(key, JSON.stringify(val))
			}
		}
	},
	// 网页字体
	webFont(fontName, select, callback) {
		const dom = Sea(select)
		dom.css({
			opacity: '0',
			transition: 'opacity 0.3s',
			'font-family': fontName,
		})
		const text = dom.text()
		if (text) {
			Sea.Ajax({
				method: 'POST',
				url: '/api.web.font',
				data: {
					text: text,
          /*
          目前支持
          'TSSunOld' 
          'STLibianSC' 
          */
					font: fontName,
				},
			}).then(res => {
				dom.css('opacity', '1')
				if (res.ok) {
					const host = Sea.Ajax.HOST || ''
					const path = host + res.path
					const className = 'webFont-' + fontName
					const webFont = Sea('.' + className).dom
					if (webFont) {
						webFont.href = path
					} else {
						Sea('head').append(`<link class="${className}" rel="stylesheet" href="${path}">`)
					}
				}
				// 执行回调
				if (typeof callback === 'function') {
					callback()
				}
			})
		} else {
			// 执行回调
			if (typeof callback === 'function') {
				callback()
			}
		}
	},
}
// 载入
for (let key in Sea.static) {
	Sea[key] = Sea.static[key]
}
// 默认 host 域名
// Sea.Ajax.HOST = 'http://127.0.0.1:1999'
// Sea 大海
window.log = log
window.Sea = Sea
// export default Sea

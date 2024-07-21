export default {
    install: function (Vue) {
        Vue.prototype.$debounce = function ( fn,delay){
            let timer = null //借助闭包
            return function() {
                if(timer){
                    clearTimeout(timer) //进入该分支语句，说明当前正在一个计时过程中，并且又触发了相同事件。所以要取消当前的计时，重新开始计时
                    timer = setTimeout(fn,delay)
                }else{
                    timer = setTimeout(fn,delay) // 进入该分支说明当前并没有在计时，那么就开始一个计时
                }
            }
        }
    }
}

/*这段代码是一个Vue插件的定义，通过`install`方法将一个自定义的函数`$debounce`添加到Vue实例的原型上。具体解析如下：

1. `export default`：这是ES6模块的导出语法，表示导出一个默认的对象。在这段代码中，默认导出的是一个对象。

2. `install`方法：这是一个插件的安装方法，在Vue插件中常见的命名约定。通过定义`install`方法，可以将自定义的功能添加到Vue实例中。

3. `Vue.prototype.$debounce`：这行代码定义了一个名为`$debounce`的方法，并将其添加到Vue原型上。
这意味着在Vue实例中的所有组件中都可以通过`this.$debounce`来调用这个方法。

4. 函数定义：这个`$debounce`方法是一个函数，接受两个参数`fn`和`delay`，`fn`代表要执行的函数，`delay`代表延迟的时间间隔。

5. 函数实现：`$debounce`函数内部使用闭包来实现防抖的功能。具体的实现逻辑如下：

   - 在函数内部定义了一个变量`timer`，用于存储定时器的引用。
   - 返回一个匿名函数作为`$debounce`的结果，这个匿名函数是真正被调用的函数。
   - 当匿名函数被调用时，首先检查`timer`变量的值。
   - 如果`timer`存在，表示前一个计时器还在运行中，需要清除之前的计时器，并重新开始计时。
   - 如果`timer`不存在，表示前一个计时器已经完成或尚未启动，直接开始一个新的计时器。
   - 使用`setTimeout`函数来延迟执行`fn`函数，延迟时间为`delay`参数指定的时间。

通过这种方式，`$debounce`函数实现了一个简单的防抖功能，用于延迟执行一个函数，并在短时间内连续触发时，
只执行最后一次触发的函数调用。这在一些需要限制频繁触发的场景下很有用，如输入框输入联想、滚动事件等。

 */
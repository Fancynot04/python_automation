## react组件
> 两种类型，函数和类组件；注意组件类只能包含一个顶层标签
```js
//1.创建一个函数组件
function HelloMessage(props) {
    return <h1>Hello {props.name}!</h1>;
}
//2.hook且传参
const element = <HelloMessage name="john"/>;
//3.标签绑定dom元素
const root = ReactDOM.createRoot(document.getElementById("root"));
//4.组件渲染
root.render(
    element
);
```

## Q: 
    1.return {} 和 return () 区别？</br>
    2.() => {}是什么，对比优缺点 ? </br>
    3.const { onChangeHandler } = this.props ? </br>
    4.useState的解构赋值 ?
    5.useEffect ?
---
## schedule
```markdown
1. 组件和JSX
2. 插值和状态
    A. <html> { 插值表达式 } </html>
    B. 通过this.state保存数组类型，方便后续直接调用值来map循环
    C. 箭头表达式
        ----------------------------------
        var f = ([params]) => expression（单一）
        // 等价于以下写法
        var f = function([params]){
            return expression;
        }
        ----------------------------------
3. 挂载和状态设置
    A. componentDidMount() 先呈现轮廓再加载数据（组件挂载完毕后，再执行）
    B. setState中console.log会先执行，导致输出之前没更新的pokemons,（异步任务）
        但可以用其中两个参数来写，其中第二个必定在第一个之后执行
4. 生命周期
    A. 注意App类中各个函数的调用顺序和次数
5. 拆组件
6. 事件处理器
    A. onChangeHandler获取事件，得到输入值
    B. 调用类方法使用this
7. props
    A. props跨文件传输变量
8. 遍历
9. CSS
    A. 列表中插入获取图片,发现第一张图片永远不变
    B. 每次筛选后，index的序号都是从0-n,采用自定义id给每个result
10. useState
    A.把类组件 改为 函数组件
    B.this无法使用，使用useState进行解构赋值
11. useEffect

```
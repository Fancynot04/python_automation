/* 
【JQuery快速入门】
1.一个JavaScript的函数库
2.更加快速的元素选择：
    $(this)当前元素
    $("p.intr") 所有class为intr的p标签
    $("ul li:first")每个ul下的第一个li元素
    $("href$='.jpg'")所有href属性结尾为.jpg的元素
3.异步加载：AJAX无刷新页面
    $.ajax({
        url:'like_comment',//请求地址
        type:'get',//请求方式
        data:{comment_id:comment_id},//传出的数据
        success:function(res){ //请求成功
            if(res=="YES")
            {
                window.location.reload();
            }else{
                window.location.reload();
            }
        },
        error:function(xhr){ //请求失败
            //请求不成功,转态码不为200的时候执行
            alert("获取数据失败!")
        }
4.JQuery的方法链：
    $("#name").css("font-size","2em").slideUp(2000).slideDown(3000).fadeOut("3000")
5.获取元素或表单的值：.val(),.text(),.html()
*/

// 选择器的简写形式（单个或多个）
const $ = v=>document.querySelector(v);
const $$ = v=>document.querySelectorAll(v);
const prevBtn = $("#prev");
const nextBtn = $("#next");
const progress = $("#progress");
const circleElements = $$(".circle");
const min=0,max=circleElements.length-1;
let currentActive = 0;

function handleClass(el){
    let methods = {
        addClass,
        removeClass
    };
    function addClass(c){
        el.classList.add(c);
        return methods;
    };
    function removeClass(c){
        el.classList.remove(c);
        return methods;
    };
    return methods;
}

function update(){
    circleElements.forEach((item,index)=>{
        if(index <= currentActive){
            item.classList.add('active');
        }else{
            item.classList.remove('active');
        }
    });
    progress.style.width = (100 / max * currentActive).toFixed(4) + '%';
}

nextBtn.addEventListener("click",()=>{
    if(nextBtn.classList.contains('disabled')) return;
    if(currentActive >= max-1){ // 0 1 2 3
        handleClass(nextBtn).addClass("disabled").removeClass("active");
    }
    if(currentActive <= max-1){
        currentActive++;
    }
    if(currentActive > 0){
        handleClass(prevBtn).addClass('active').removeClass('disabled')
    }
    update();
});

prevBtn.addEventListener("click",()=>{
    if(prevBtn.classList.contains('disabled')) return;
    if(currentActive <= 1){
        handleClass(prevBtn).addClass("disabled").removeClass("active");
    }
    if(currentActive > 0){
        currentActive--;
    }
    if(currentActive <= max-1){
        handleClass(nextBtn).addClass("active").removeClass("disabled");
    }
    update();
});
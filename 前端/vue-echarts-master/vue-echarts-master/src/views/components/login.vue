

<template>
  <div class="box">
    <div class="register">
      <img src="../../assets/less/login.jpg" style="width: 250px;height: 150px;margin-left: 26%"/>
      <el-form ref="form" :model="form" :rules="rules"  label-width="30px" class="from">
        <el-form-item label="">
          <el-input prefix-icon="el-icon-user" placeholder="输入登录账户" v-model.number="form.name"></el-input>
        </el-form-item>
        <el-form-item label="" prop="psw">
          <el-input autocomplete="off" prefix-icon="el-icon-lock" placeholder="输入登录密码" show-password v-model.number="form.psw"></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" :round=false :plain=false class="buttonres" @click="reg('form')">登录</el-button>
      <div class="login">已有账号，
        <router-link to="/register">注册</router-link>
        <span style="margin-left: 10%; font-size:13px">请前往注册界面进行注册</span>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import request from "@/utils/request";
export default {
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        if (this.form.pswok !== '') {
          this.$refs.form.validateField('pswok');
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.form.psw) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      isforbidden:false,
      form:{
        name: '',
        verify:'',
        psw:'',
        pswok:'',
        email:""
      },
      rules: {
        psw: [
          { validator: validatePass, trigger: 'blur' }
        ],
        pswok: [
          { validator: validatePass2, trigger: 'blur' }
        ],
      }
    };
  },

  methods:{
    reg(form){
      this.$refs[form].validate((valid) => {
        if (valid) {

          request.get("http://127.0.0.1:5000/login?username=" + this.form.name + "&password=" + this.form.psw).then(res => {
            if(res.data==true){
              this.$message({
                message: '登录成功',
                type: 'success'
              })
              setTimeout(() => {
                this.$router.push("/page2")
              }, 1500);
            }else{
              this.$message({
                message: '登录失败',
                type: 'error'
              })
            }
          })
        } else {
          this.$alert('请输入完整内容', '提示', {
            confirmButtonText: '确定',
            // eslint-disable-next-line no-unused-vars
            callback: action => {
              this.$message({
                type: 'error',
                message: `错误: ${ "请输入完整信息" }`
              });
            }
          });
          return false;
        }
      });
      // console.log(this.form.name);
    },
    //发送验证码
    verificationcode(e){
      if(this.form.email==''){
        this.$message.error('没有输入邮箱');
      }else{
        axios({
          url:"http://127.0.0.1:5000/emails",
          method:"POST",
          data:{
            email : this.form.email,
          }
        }).then((res)=>{
          console.log(res.data);
          // eslint-disable-next-line no-unused-vars
        },(err)=>{
          console.log("请求错误");
        })
        this.isforbidden=true;
        let k = 60;
        let time = setInterval(()=>{
          if(k==0){
            e.target.innerHTML="获取验证码";
            this.isforbidden = false;
            clearInterval(time);
          }else{
            e.target.innerHTML="还剩"+k+"秒";
            k--;
          }
        },1000)
      }
    }
  }
}
</script>

<style scoped>
.box{
  height: 100%;
  background-image: url(../../assets/zc.jpg);
  background-repeat: no-repeat;
  background-size: cover;
}
.register{
  width: 35%;
  height: 80%;
  background-color: #fff;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%,-50%);
  border-radius: 5px;
}
footer{
  font-family: '宋体';
  font-size: 24px;
  text-align: center;
  padding-top: 50px;
}
.from{
  width: 75%;
  margin: 0 auto;
  margin-right: 15%;
  margin-top: 8%;
}
.inputtow{
  width: 65%;
}

.buttonVerify{
  position: absolute;
  left: 64%;
  top: 31%;
}
.buttonres{
  width: 70%;
  margin-left: 15%;
  margin-top: 5%;
}
.login{
  margin-left: 15%;
  margin-top: 5%;
  color: #ccc;
  font: size 13px;
}
</style>

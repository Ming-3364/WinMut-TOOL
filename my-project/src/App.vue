<template>
<el-container style="height: 100%;">
  <!-- side bar -->
  <el-aside width="200px">
    <!-- subject selector -->
    <el-dropdown @command="selectSubject">
      <el-button type="primary">
        Subject<i class="el-icon-arrow-down el-icon--right">{{ curSubject }}</i>
      </el-button>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="demo">Demo</el-dropdown-item>
        <el-dropdown-item>Pcre2</el-dropdown-item>
        <el-dropdown-item>Grep</el-dropdown-item>
        <el-dropdown-item disabled>Coreutils</el-dropdown-item>
        <el-dropdown-item divided>xxx</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>

    <!-- subject foleders -->
    <el-tree
        :data="foldersData"
        @node-click="handleFileClick"
      >
    </el-tree>
  </el-aside>

  <!-- run, code, and result -->
  <el-container>

    <!-- run -->
    <el-header>
      <el-row type="flex" justify="space-between">
        <!-- 左对齐的按钮组 -->
        <el-col>
          <el-button type="primary" @click="runCaseConfigDrawer = true">Run Case Config</el-button>
          <el-drawer
            title="Run Case Config"
            :visible.sync="runCaseConfigDrawer"
            :direction="runCaseConfigDrawerDirection"
            size='40%'
            :before-close="handleClose">
            <el-form :model="runCaseConfigForm" ref="runCaseConfigForm" label-width="100px" class="demo-dynamic">
              <el-form-item
                v-for="(runCase, index) in runCaseConfigForm"
                :label="'Case' + index"
                :key="runCase.key"
                :rules="{
                }"
              >
                <el-form :inline="true" :model="runCaseConfigForm[index]" class="demo-form-inline">
                  <el-form-item label="file">
                    <!-- TODO: rule for check input run case config -->
                    <el-select v-model="runCase.file" placeholder="file">
                      <el-option 
                        v-for="file in foldersData"
                        :label=file.label
                        :key=file.label
                        :value="file.label"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="argvs">
                    <el-input v-model="runCase.argv" placeholder="argvs"></el-input>
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button type="primary" @click="delRunCase(index)">删除</el-button>
                  </el-form-item>
                </el-form>
              </el-form-item>
              <el-form-item>
                <el-button  type="primary" @click="addRunCase">新增</el-button>
                <el-button  type="primary" @click="resetRunCase()">重置</el-button>
              </el-form-item>
            </el-form>
            {{ runCaseConfigForm }}
            <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="100px" class="demo-dynamic">
              <el-form-item
                v-for="(domain, index) in dynamicValidateForm.domains"
                :label="'域名' + index"
                :key="domain.key"
                :prop="'domains.' + index + '.value'"
                :rules="{
                  required: true, message: '域名不能为空', trigger: 'blur'
                }"
              >
                <el-input v-model="domain.value" style="width: 100px;"></el-input><el-button @click.prevent="removeDomain(domain)">删除</el-button>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button>
                <el-button @click="addDomain">新增域名</el-button>
                <el-button @click="resetForm('dynamicValidateForm')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-drawer>
        </el-col>

        <!-- 右对齐的按钮组 -->
        <el-col style="text-align: right;">
          <el-button type="primary" @click="submitRunCaseConfigForm">Run</el-button>
        </el-col>
      </el-row>
    </el-header>

    <!-- code and result -->
    <el-container>

      <!-- code -->
      <el-main style="width: 50%;">
        <el-input
          type="textarea" 
          :rows="32"
          placeholder="请输入代码"
          v-model="cur_file_content"
          show-password
        ></el-input>
      </el-main>

      <!-- result -->
      <el-main style="width: 50%;">
        <el-tabs type="border-card" stretch="true" style="height: 90%;" >

          <!-- OUTPUT -->
          <el-tab-pane label="OUTPUT" >
            <el-tabs v-model="activeOutputTab" style="height: 90%;">
              <el-tab-pane
                
                v-for="(mutOutputFilesForCase, caseName, index) in mutOutputFilesForRun"
                :label="caseName"
                :name="caseName"
                :key="index"
              >
                <!-- tab content -->
                <el-container style="height: 100%;">
                  <!-- 左侧文件选择栏 -->
                  <el-aside width="200px" style="height: 100%;">
                  <el-scrollbar style="height: 100%;">
                    <el-menu
                      style="height: 100%;"
                      @select="handleMutOutputFileSelect"
                      :default-active="activeFileGroupIndex"
                    >
                      <el-submenu
                        v-for="(files, fileGroup, index) in mutOutputFilesForCase.mutOutputFiles"
                        :title="fileGroup"
                        :key="index"
                        :index="index"
                      >
                        <!-- <template slot="title"> -->
                          <!-- <i class="el-icon-location"></i> -->
                          <span slot="title">{{fileGroup}}</span>
                        <!-- </template> -->
                        <el-menu-item 
                          v-for="file in files" 
                          :key="file.name" 
                          :index="file.name"
                          @click="handleSelectMutOutputFile(file)"
                        >
                          {{ file.name }}
                        </el-menu-item>
                      </el-submenu>
                    </el-menu>
                  </el-scrollbar>
                  </el-aside>

                  <!-- 右侧文件内容显示区域 -->
                  <el-main>
                    <!-- <codemirror v-model="selectedMutOutputContent" :options="editorOptions">{{selectedMutOutputContent}}</codemirror> -->
                    <el-input
                      type="textarea"
                      :rows="22"
                      placeholder="please select a mut output file"
                      v-model="selectedMutOutputContent"

                      :disabled="false">
                    </el-input>
                  </el-main>
                </el-container>
              </el-tab-pane>
            </el-tabs>
          </el-tab-pane>
          
          <!-- STATS -->
          <el-tab-pane label="STATS">
            <el-tabs v-model="activeStatTab" style="height: 90%;">
              <el-tab-pane
                label="Summary"
                name="Summary"
                key="Summary"
              >
              {{ runStat.Summary }}
              </el-tab-pane>

              <el-tab-pane
                
                v-for="(caseInfo, caseName) in runStat.MACases"
                :label="caseName"
                :name="caseName"
                :key="caseName"
              >
              {{ caseInfo }}
              </el-tab-pane>
            </el-tabs>
          </el-tab-pane>

        </el-tabs>
      </el-main>

    </el-container>
    
  </el-container>
</el-container>
</template>

<!-- <template>
<div id="app" style="height: 100vh;">
<el-row style="height: 100vh;">
  <el-col :span="12"><div class="grid-content bg-purple">main1</div></el-col>
  <el-col :span="12"><div class="grid-content bg-purple-light">main2</div></el-col>
</el-row>
<el-row style="height: 100vh;">
  <el-col :span="8"><div class="grid-content bg-purple">main3</div></el-col>
  <el-col :span="8"><div class="grid-content bg-purple-light">main4</div></el-col>
  <el-col :span="8"><div class="grid-content bg-purple">main5</div></el-col>
</el-row>
</div>
</template> -->

<style scoped>
* {
  /* border: 1px solid #ddd; */
}




</style>

<script>
// import codemirror
// import { codemirror } from 'vue-codemirror';
import 'codemirror/lib/codemirror.css';

export default {
  data() {
    return {
      curSubject: "demo",
      // subject folders
      foldersData: [
        {
          id: 1,
          label: 'file1',
        },
        {
          id: 2,
          label: 'file2',
        },
        {
          id: 3,
          label: 'file5',
        }
      ],
      selectedNodeLabel: '',

      // code
      cur_file_content: '',

      // run case config
      runCaseConfigDrawer: false,
      runCaseConfigDrawerDirection: 'ttb',
      
      defaultRunCaseConfigForm: [
        {
          file: 'quick_sort',
          argv: '11 22 33 44 55 66'
        },
        {
          file: 'quick_sort',
          argv: '11 22 33 44 55 66'
        },
      ],

      runCaseConfigForm: [
        {
          file: 'quick_sort',
          argv: '11 22 33 44 55 66'
        }
      ],

      dynamicValidateForm: {
        domains: [{
          value: ''
        }],
        email: ''
      },

      // OUTPUT
      activeOutputTab: 'case_1', // 设置默认激活的标签
      outputTabsData: [
        { label: '标签1', name: 'tab1', content: '标签1的内容' },
        { label: '标签2', name: 'tab2', content: '标签2的内容' },
        { label: '标签2', name: 'tab2', content: '标签2的内容' },
        { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // { label: '标签2', name: 'tab2', content: '标签2的内容' },
        // 其他标签数据...
      ],

      files: ['file1.txt', 'file2.txt', 'file3.txt'],
      selectedFile: '',
      fileContent: '',
      editorOptions: {
        lineNumbers: true,
        mode: 'text/plain',
        theme: 'base16-dark'
      },
      
      mutOutputFilesForRun: {
        "case_1": {
              "case_dir": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1",
              "mutOutputFiles": {
                  "stdoutcopy": [
                      {
                          "name": "mut_output-0-stdoutcopy",
                          "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-0-stdoutcopy"
                      },
                      {
                          "name": "mut_output-339-stdoutcopy",
                          "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
                      },
                  ]
          }
        },
        "case_2": {
              "case_dir": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1",
              "mutOutputFiles": {
                  "stdoutcopy": [
                      {
                          "name": "mut_output-0-stdoutcopy",
                          "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-0-stdoutcopy"
                      },
                      {
                          "name": "mut_output-339-stdoutcopy",
                          "path": "/home/bjtucs/Desktop/Ming-18811237867/new/WinMutASE21Artifact-main/experiments/web-tool/web-run/2024-01-15-20-13-05/log/run/case_1/mut_output-339-stdoutcopy"
                      },
                  ]
          }
        },
      },
      activeFileGroupIndex: '0',
      selectedMutOutputContent: 'asdfasdf',

      // STATS
      activeStatTab: 'Summary',
      runStat: {
        "MACases": {
            "case_2": {
                "case_name": "./bin/demo-fibonacci",
                "covered": 85,
                "generated": 85,
                "killed": 76,
                "killed_by_both": 20,
                "killed_by_proc_end_status": 20,
                "killed_by_proc_output": 76,
                "ms_k2c": 0.8941176470588236,
                "ms_k2g": 0.8941176470588236,
                "survived_by_both": 0,
                "survived_not_affect_output": 0,
                "survived_not_affect_status": 9,
                "survived_not_covered": 0,
                "uncovered": 0
            },
            "case_3": {
                "case_name": "./bin/demo-mut_output-carrymut",
                "covered": 39,
                "generated": 39,
                "killed": 31,
                "killed_by_both": 15,
                "killed_by_proc_end_status": 15,
                "killed_by_proc_output": 31,
                "ms_k2c": 0.7948717948717948,
                "ms_k2g": 0.7948717948717948,
                "survived_by_both": 0,
                "survived_not_affect_output": 0,
                "survived_not_affect_status": 8,
                "survived_not_covered": 0,
                "uncovered": 0
            },
            "case_4": {
                "case_name": "./bin/demo-quick_sort",
                "covered": 373,
                "generated": 794,
                "killed": 285,
                "killed_by_both": 175,
                "killed_by_proc_end_status": 175,
                "killed_by_proc_output": 285,
                "ms_k2c": 0.7640750670241286,
                "ms_k2g": 0.3589420654911839,
                "survived_by_both": 12,
                "survived_not_affect_output": 12,
                "survived_not_affect_status": 88,
                "survived_not_covered": 421,
                "uncovered": 421
            }
        },
        "Summary": {
            "ms_k2c_avg": 0.8176881696515824,
            "ms_k2c_max": 0.8941176470588236,
            "ms_k2c_med": 0.7948717948717948,
            "ms_k2c_min": 0.7640750670241286,
            "ms_k2g_avg": 0.6826438358072675,
            "ms_k2g_max": 0.8941176470588236,
            "ms_k2g_med": 0.7948717948717948,
            "ms_k2g_min": 0.3589420654911839
        }
      }
    };
  },
  mounted() {
    // init run case config form
    this.runCaseConfigForm = this.defaultRunCaseConfigForm;
  },

  methods: {

    handleMutOutputFileSelect(){

    },

    handleSelectMutOutputFile(file){
      this.$axios.post('/api/get_file_content', { file_path: file.path })
        .then(response => {
          console.log("get file content", file.path)
          this.selectedMutOutputContent = response.data.content;
          console.log(response.data.content)
        })
        .catch(error => {
          console.error('Error fetching file content:', error);
        });
    },

    submitRunCaseConfigForm(){
      this.$axios.post('/api/web_run', this.runCaseConfigForm)
        .then(response => {
          alert("run complete")
          this.mutOutputFilesForRun = response.data.mutOutputFilesForRun;
          this.runStat = response.data.runStat
          console.log(response)
        })
        .catch(error => {
          console.error('Error fetching file content:', error);
        });
    },

    addRunCase() {
      this.runCaseConfigForm.push(
        {
          file: '',
          argv: '',
        }
      )
    },

    delRunCase(index) {
      this.runCaseConfigForm.splice(index, 1);
    },

    resetRunCase(){
      // reset run case config form
      this.runCaseConfigForm = [].concat(this.defaultRunCaseConfigForm);
    },

    submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    removeDomain(item) {
      var index = this.dynamicValidateForm.domains.indexOf(item)
      if (index !== -1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain() {
      this.dynamicValidateForm.domains.push({
        value: '',
        key: Date.now()
      });
    },


    async getFileContent() {
      try {
        // const response = await this.$axios.get('/api/get_file_content');
        // this.fileContent = response.data.content;
        
        await this.$axios
          .get('/api/get_file_content')
          .then(response => (this.fileContent = response.data.content))
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });

      } catch (error) {
        console.error('Error fetching file content:', error);
      }
    },

    // getFileContent(file_path) {
    //   this.$axios.post('/api/get_file_content', { file_path: filePath })
    //     .then(response => {
    //       this.fileContent = response.data.content;
    //     })
    //     .catch(error => {
    //       console.error('Error fetching file content:', error);
    //     });
    // },

    async handleFileClick(data) {
      console.log(data.label)
      console.log(data.path)
      this.$axios.post('/api/get_file_content', { file_path: data.path })
        .then(response => {
          this.cur_file_content = response.data.content;
          console.log(response.data.content)
        })
        .catch(error => {
          console.error('Error fetching file content:', error);
        });
    },

    selectSubject(command) {
      if (command === "demo") {
        this.getDemoSrc()
      }
    },

    async getDemoSrc() {
      try {
        console.log("get demo src\n")
        await this.$axios
          .get('/api/get_demo_src')
          .then(response => (this.foldersData = response.data.data))
          .catch(function (error) { // 请求失败处理
            console.log(error);
          });

      } catch (error) {
        console.error('Error getting demo src:', error);
      }
    }
  },

  
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
}
</style>

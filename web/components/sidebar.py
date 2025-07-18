"""
侧边栏组件
"""

import streamlit as st
import os

def render_sidebar():
    """渲染侧边栏配置"""

    with st.sidebar:
        # AI模型配置
        st.markdown("### 🧠 AI模型配置")

        # LLM提供商选择
        llm_provider = st.selectbox(
            "LLM提供商",
            options=["dashscope", "deepseek", "google", "openai"],
            index=0,
            format_func=lambda x: {
                "dashscope": "阿里百炼",
                "deepseek": "DeepSeek V3",
                "google": "Google AI",
                "openai": "OpenAI"
            }[x],
            help="选择AI模型提供商"
        )

        # 根据提供商显示不同的模型选项
        if llm_provider == "dashscope":
            llm_model = st.selectbox(
                "模型版本",
                options=["qwen-turbo", "qwen-plus-latest", "qwen-max"],
                index=1,
                format_func=lambda x: {
                    "qwen-turbo": "Turbo - 快速",
                    "qwen-plus-latest": "Plus - 平衡",
                    "qwen-max": "Max - 最强"
                }[x],
                help="选择用于分析的阿里百炼模型"
            )
        elif llm_provider == "deepseek":
            llm_model = st.selectbox(
                "选择DeepSeek模型",
                options=["deepseek-chat", "gpt-4.1", "gemini-2.5-pro-preview-06-05"],
                index=0,
                format_func=lambda x: {
                    "deepseek-chat": "DeepSeek Chat - 通用对话模型，适合股票分析",
                    "gpt-4.1": "GPT-4.1 - 强大性能",
                    "gemini-2.5-pro-preview-06-05": "Gemini 2.5 Pro - 最新预览版"
                }[x],
                help="选择用于分析的DeepSeek模型"
            )
        elif llm_provider == "google":
            llm_model = st.selectbox(
                "选择Google模型",
                options=["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
                index=0,
                format_func=lambda x: {
                    "gemini-2.0-flash": "Gemini 2.0 Flash - 推荐使用",
                    "gemini-1.5-pro": "Gemini 1.5 Pro - 强大性能",
                    "gemini-1.5-flash": "Gemini 1.5 Flash - 快速响应"
                }[x],
                help="选择用于分析的Google Gemini模型"
            )
        else:  # openai
            # OpenAI配置
            llm_model = st.selectbox(
                "选择OpenAI模型",
                options=["gpt-4.1", "gemini-2.5-pro-preview-06-05"],
                index=0,
                format_func=lambda x: {
                    "gpt-4.1": "GPT-4 - 最强性能",
                    "gemini-2.5-pro-preview-06-05": "Gemini 2.5 Pro - 最新预览版"
                }[x],
                help="选择用于分析的OpenAI模型"
            )
        
        # 高级设置
        with st.expander("⚙️ 高级设置"):
            enable_memory = st.checkbox(
                "启用记忆功能",
                value=False,
                help="启用智能体记忆功能（可能影响性能）"
            )
            
            enable_debug = st.checkbox(
                "调试模式",
                value=False,
                help="启用详细的调试信息输出"
            )
            
            max_tokens = st.slider(
                "最大输出长度",
                min_value=1000,
                max_value=8000,
                value=4000,
                step=500,
                help="AI模型的最大输出token数量"
            )
        
        st.markdown("---")

        # 系统配置
        st.markdown("**🔧 系统配置**")

        # API密钥状态
        st.markdown("**🔑 API密钥状态**")

        def validate_api_key(key, expected_format):
            """验证API密钥格式"""
            if not key:
                return "未配置", "error"

            if expected_format == "dashscope" and key.startswith("sk-") and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "deepseek" and key.startswith("sk-") and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "finnhub" and len(key) >= 20:
                return f"{key[:8]}...", "success"
            elif expected_format == "tushare" and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "google" and key.startswith("AIza") and len(key) >= 32:
                return f"{key[:8]}...", "success"
            elif expected_format == "openai" and key.startswith("sk-") and len(key) >= 40:
                return f"{key[:8]}...", "success"
            elif expected_format == "anthropic" and key.startswith("sk-") and len(key) >= 40:
                return f"{key[:8]}...", "success"
            elif expected_format == "reddit" and len(key) >= 10:
                return f"{key[:8]}...", "success"
            else:
                return f"{key[:8]}... (格式异常)", "warning"

        # 必需的API密钥
        st.markdown("*必需配置:*")

        # 阿里百炼
        dashscope_key = os.getenv("DASHSCOPE_API_KEY")
        status, level = validate_api_key(dashscope_key, "dashscope")
        if level == "success":
            st.success(f"✅ 阿里百炼: {status}")
        elif level == "warning":
            st.warning(f"⚠️ 阿里百炼: {status}")
        else:
            st.error("❌ 阿里百炼: 未配置")

        # FinnHub
        finnhub_key = os.getenv("FINNHUB_API_KEY")
        status, level = validate_api_key(finnhub_key, "finnhub")
        if level == "success":
            st.success(f"✅ FinnHub: {status}")
        elif level == "warning":
            st.warning(f"⚠️ FinnHub: {status}")
        else:
            st.error("❌ FinnHub: 未配置")

        # 可选的API密钥
        st.markdown("*可选配置:*")

        # DeepSeek
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        status, level = validate_api_key(deepseek_key, "deepseek")
        if level == "success":
            st.success(f"✅ DeepSeek: {status}")
        elif level == "warning":
            st.warning(f"⚠️ DeepSeek: {status}")
        else:
            st.info("ℹ️ DeepSeek: 未配置")

        # Tushare
        tushare_key = os.getenv("TUSHARE_TOKEN")
        status, level = validate_api_key(tushare_key, "tushare")
        if level == "success":
            st.success(f"✅ Tushare: {status}")
        elif level == "warning":
            st.warning(f"⚠️ Tushare: {status}")
        else:
            st.info("ℹ️ Tushare: 未配置")

        # Google AI
        google_key = os.getenv("GOOGLE_API_KEY")
        status, level = validate_api_key(google_key, "google")
        if level == "success":
            st.success(f"✅ Google AI: {status}")
        elif level == "warning":
            st.warning(f"⚠️ Google AI: {status}")
        else:
            st.info("ℹ️ Google AI: 未配置")

        # OpenAI (如果配置了且不是默认值)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key_here":
            status, level = validate_api_key(openai_key, "openai")
            if level == "success":
                st.success(f"✅ OpenAI: {status}")
            elif level == "warning":
                st.warning(f"⚠️ OpenAI: {status}")

        # Anthropic (如果配置了且不是默认值)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
            status, level = validate_api_key(anthropic_key, "anthropic")
            if level == "success":
                st.success(f"✅ Anthropic: {status}")
            elif level == "warning":
                st.warning(f"⚠️ Anthropic: {status}")

        st.markdown("---")

        # 系统信息
        st.markdown("**ℹ️ 系统信息**")
        
        st.info(f"""
        **版本**: 1.0.0
        **框架**: Streamlit + LangGraph
        **AI模型**: {llm_provider.upper()} - {llm_model}
        **数据源**: Tushare + FinnHub API
        """)
        
        # 帮助链接
        st.markdown("**📚 帮助资源**")
        
        st.markdown("""
        - [📖 使用文档](https://github.com/TauricResearch/TradingAgents)
        - [🐛 问题反馈](https://github.com/TauricResearch/TradingAgents/issues)
        - [💬 讨论社区](https://github.com/TauricResearch/TradingAgents/discussions)
        - [🔧 API密钥配置](../docs/security/api_keys_security.md)
        """)
    
    return {
        'llm_provider': llm_provider,
        'llm_model': llm_model,
        'enable_memory': enable_memory,
        'enable_debug': enable_debug,
        'max_tokens': max_tokens,
        'openai_base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    }

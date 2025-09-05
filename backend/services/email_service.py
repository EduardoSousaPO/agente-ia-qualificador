#!/usr/bin/env python3
"""
Serviço de Email via SMTP
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
import structlog

logger = structlog.get_logger()

class EmailService:
    def __init__(self):
        """Inicializar serviço de email"""
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_pass = os.getenv('SMTP_PASS', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        
        # Verificar se as configurações estão presentes
        if not all([self.smtp_user, self.smtp_pass]):
            logger.warning("Configurações SMTP não encontradas - emails não serão enviados")
            self.enabled = False
        else:
            self.enabled = True

    def send_qualified_lead_email(self, lead_data: Dict, consultant_email: str) -> Dict:
        """Enviar email de notificação sobre lead qualificado"""
        try:
            if not self.enabled:
                logger.info("SMTP desabilitado - simulando envio de email", 
                           lead_name=lead_data.get('name'),
                           consultant_email=consultant_email)
                return {
                    'success': True,
                    'message': 'Email simulado (SMTP desabilitado)',
                }

            # Preparar conteúdo do email
            subject = f"🎯 Lead Qualificado: {lead_data.get('name', 'Sem nome')}"
            
            html_body = self._build_email_template(lead_data)
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = consultant_email
            
            # Adicionar conteúdo HTML
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            logger.info("Email de lead qualificado enviado", 
                       lead_id=lead_data.get('id'),
                       lead_name=lead_data.get('name'),
                       consultant_email=consultant_email,
                       score=lead_data.get('score'))
            
            return {
                'success': True,
                'message': 'Email enviado com sucesso'
            }
            
        except Exception as e:
            logger.error("Erro ao enviar email", 
                        lead_id=lead_data.get('id'),
                        consultant_email=consultant_email,
                        error=str(e))
            return {
                'success': False,
                'error': f'Erro ao enviar email: {str(e)}'
            }

    def _build_email_template(self, lead_data: Dict) -> str:
        """Construir template HTML do email"""
        name = lead_data.get('name', 'Sem nome')
        email = lead_data.get('email', 'Não informado')
        phone = lead_data.get('phone', 'Não informado')
        score = lead_data.get('score', 0)
        origem = lead_data.get('origem', 'WhatsApp')
        
        # Determinar cor baseada no score
        if score >= 90:
            score_color = "#059669"  # Verde forte
            score_label = "EXCELENTE"
        elif score >= 80:
            score_color = "#0891b2"  # Azul
            score_label = "MUITO BOM"
        else:
            score_color = "#ea580c"  # Laranja
            score_label = "BOM"

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lead Qualificado</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">🎯 Lead Qualificado</h1>
                    <p style="color: #e2e8f0; margin: 10px 0 0 0; font-size: 14px;">Agente Qualificador IA</p>
                </div>
                
                <!-- Score Badge -->
                <div style="text-align: center; padding: 20px; background-color: #f8fafc;">
                    <div style="display: inline-block; background-color: {score_color}; color: white; padding: 12px 24px; border-radius: 50px; font-weight: bold; font-size: 18px;">
                        SCORE: {score}/100 - {score_label}
                    </div>
                </div>
                
                <!-- Lead Info -->
                <div style="padding: 30px;">
                    <h2 style="color: #1f2937; margin: 0 0 20px 0; font-size: 20px;">Informações do Lead</h2>
                    
                    <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; border-left: 4px solid {score_color};">
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; font-weight: 600; color: #374151; width: 120px;">Nome:</td>
                                <td style="padding: 8px 0; color: #1f2937;">{name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: 600; color: #374151;">Email:</td>
                                <td style="padding: 8px 0; color: #1f2937;">{email}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: 600; color: #374151;">Telefone:</td>
                                <td style="padding: 8px 0; color: #1f2937;">{phone}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: 600; color: #374151;">Origem:</td>
                                <td style="padding: 8px 0; color: #1f2937;">{origem}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <!-- CTA Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://wa.me/{phone.replace('+', '').replace(' ', '').replace('-', '')}" 
                           style="display: inline-block; background-color: #10b981; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">
                            📱 Entrar em Contato via WhatsApp
                        </a>
                    </div>
                    
                    <div style="background-color: #fef3c7; border: 1px solid #fbbf24; border-radius: 6px; padding: 16px; margin: 20px 0;">
                        <p style="margin: 0; color: #92400e; font-size: 14px;">
                            <strong>⚡ Ação Recomendada:</strong> Entre em contato com este lead o mais rápido possível. 
                            Leads com score alto têm maior probabilidade de conversão quando contactados rapidamente.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #f1f5f9; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="margin: 0; color: #64748b; font-size: 12px;">
                        Este email foi gerado automaticamente pelo Agente Qualificador IA<br>
                        Sistema de Qualificação de Leads via WhatsApp
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template

    def send_test_email(self, to_email: str) -> Dict:
        """Enviar email de teste"""
        try:
            if not self.enabled:
                return {
                    'success': True,
                    'message': 'Email de teste simulado (SMTP desabilitado)',
                }

            subject = "🧪 Teste - Agente Qualificador IA"
            body = """
            <h2>Email de Teste</h2>
            <p>Este é um email de teste do sistema Agente Qualificador IA.</p>
            <p>Se você recebeu este email, a configuração SMTP está funcionando corretamente!</p>
            <p><strong>Data/Hora:</strong> {}</p>
            """.format(str(os.getenv('CURRENT_DATETIME', 'N/A')))
            
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            logger.info("Email de teste enviado", to_email=to_email)
            
            return {
                'success': True,
                'message': 'Email de teste enviado com sucesso'
            }
            
        except Exception as e:
            logger.error("Erro ao enviar email de teste", to_email=to_email, error=str(e))
            return {
                'success': False,
                'error': f'Erro ao enviar email de teste: {str(e)}'
            }

# Instância global
email_service = EmailService()


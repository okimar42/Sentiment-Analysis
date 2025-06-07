import React from 'react';
import { Paper, Typography } from '@mui/material';
import type { BotAnalysis } from '../../services/api';

interface BotAnalysisCardProps {
  botAnalysis: BotAnalysis | null;
}

export const BotAnalysisCard: React.FC<BotAnalysisCardProps> = ({ botAnalysis }) => {
  if (!botAnalysis) {
    return null;
  }

  return (
    <Paper style={{ padding: '20px' }}>
      <Typography variant="h6" gutterBottom>
        Bot Analysis
      </Typography>
      <Typography>Total Posts: {botAnalysis.total || 0}</Typography>
      <Typography>Detected Bots: {botAnalysis.bots || 0}</Typography>
      <Typography>Non-Bot Posts: {botAnalysis.not_bots || 0}</Typography>
      <Typography>
        Average Bot Probability: {(botAnalysis.avg_bot_probability * 100 || 0).toFixed(1)}%
      </Typography>
    </Paper>
  );
};
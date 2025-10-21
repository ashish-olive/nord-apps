import React, { useState, useEffect } from 'react';
import { Container, Grid, Typography, Tabs, Tab, Box, Alert, CircularProgress } from '@mui/material';
import ScenarioForm from '../components/ScenarioForm';
import ScenarioResult from '../components/ScenarioResult';
import { usageApi } from '../api/usageApi';

const ScenarioStudio = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [result, setResult] = useState(null);
  const [providers, setProviders] = useState([]);
  const [providerPricing, setProviderPricing] = useState({});
  const [baseline, setBaseline] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [providersRes, summaryRes] = await Promise.all([
        usageApi.getProviders(),
        usageApi.getExecutiveSummary(30),
      ]);
      const providerList = providersRes.data.providers;
      setProviders(providerList.map(p => p.name));
      
      // Create pricing lookup
      const pricing = {};
      providerList.forEach(p => {
        pricing[p.name] = {
          monthly: p.cost_per_server_monthly,
          transfer: p.cost_per_gb_transfer,
        };
      });
      setProviderPricing(pricing);
      setBaseline(summaryRes.data.metrics);
    } catch (error) {
      console.error('Error loading scenario data:', error);
    } finally {
      setLoading(false);
    }
  };

  const scenarios = [
    {
      type: 'server_scaling',
      title: 'Server Scaling',
      description: 'Model the usage impact of adding or removing servers from a specific cloud provider.',
      helpText: 'Enter a positive number to add servers or a negative number to remove servers. Select the provider where you want to scale.',
      fields: [
        { name: 'server_change', label: 'Number of Servers to Add/Remove', type: 'number', helperText: 'Use negative numbers to remove servers' },
        { name: 'provider', label: 'Provider', type: 'select', options: providers },
      ],
    },
    {
      type: 'provider_migration',
      title: 'Provider Migration',
      description: 'Calculate potential savings by migrating servers from one cloud provider to another.',
      helpText: 'Select the source and destination providers, then specify what percentage of servers to migrate.',
      fields: [
        { name: 'from_provider', label: 'From Provider', type: 'select', options: providers },
        { name: 'to_provider', label: 'To Provider', type: 'select', options: providers },
        { name: 'server_percentage', label: 'Percentage of Servers to Migrate', type: 'number', helperText: 'Enter a value between 0-100' },
      ],
    },
    {
      type: 'traffic_growth',
      title: 'Traffic Growth',
      description: 'Forecast infrastructure usage based on expected traffic growth.',
      helpText: 'Enter the expected percentage increase in traffic. The model will calculate additional infrastructure usage needed.',
      baseline: baseline ? {
        current_sessions: baseline.total_sessions,
        current_cost: baseline.total_cost?.value,
      } : null,
      fields: [
        { name: 'growth_percentage', label: 'Expected Growth Percentage', type: 'number', helperText: 'E.g., enter 25 for 25% growth' },
      ],
    },
    {
      type: 'cost_optimization',
      title: 'Usage Optimization',
      description: 'Estimate savings from specific infrastructure optimization initiatives.',
      helpText: 'Select optimization strategies to model their combined impact on infrastructure usage.',
      baseline: baseline ? {
        current_cost: baseline.total_cost?.value,
        base_cost: baseline.base_cost?.value,
        current_sessions: baseline.total_sessions,
      } : null,
      fields: [
        { 
          name: 'right_sizing', 
          label: 'Right-size Over-provisioned Instances', 
          type: 'select', 
          options: ['None', 'Conservative (5-10%)', 'Moderate (10-15%)', 'Aggressive (15-20%)'],
          helperText: 'Reduce instance sizes for underutilized servers'
        },
        { 
          name: 'reserved_instances', 
          label: 'Reserved/Committed Use Discounts', 
          type: 'select', 
          options: ['None', '1-Year Commitment (15%)', '3-Year Commitment (30%)'],
          helperText: 'Commit to long-term usage for discounts'
        },
        { 
          name: 'spot_instances', 
          label: 'Use Spot/Preemptible Instances', 
          type: 'select', 
          options: ['None', 'Non-Critical Workloads (20%)', 'Batch Processing (40%)'],
          helperText: 'Use interruptible instances for flexible workloads'
        },
        { 
          name: 'auto_scaling', 
          label: 'Implement Auto-scaling', 
          type: 'select', 
          options: ['None', 'Basic (5-8%)', 'Advanced (10-15%)'],
          helperText: 'Scale resources based on actual demand'
        },
      ],
    },
  ];

  const handleScenarioSubmit = async (formData) => {
    // Mock scenario calculation - in real app, call backend API
    console.log('Scenario:', scenarios[activeTab].type, formData);
    
    const scenarioType = scenarios[activeTab].type;
    const baselineCost = baseline?.total_cost?.value || 50000;
    
    // Calculate based on scenario type
    let projectedCost, savings, changePercent, explanation, details;
    
    switch (scenarioType) {
      case 'server_scaling':
        const serverChange = parseInt(formData.server_change) || 0;
        const costPerServer = 150; // Average monthly cost per server
        const monthlyCostChange = serverChange * costPerServer;
        projectedCost = baselineCost + monthlyCostChange;
        savings = -monthlyCostChange;
        changePercent = (monthlyCostChange / baselineCost) * 100;
        explanation = serverChange > 0 
          ? `Adding ${serverChange} servers on ${formData.provider} will increase monthly costs by approximately $${Math.abs(monthlyCostChange).toFixed(2)}.`
          : `Removing ${Math.abs(serverChange)} servers from ${formData.provider} will reduce monthly costs by approximately $${Math.abs(monthlyCostChange).toFixed(2)}.`;
        details = [
          `Estimated cost per server: $${costPerServer}/month`,
          `Total ${serverChange > 0 ? 'additional' : 'reduced'} cost: $${Math.abs(monthlyCostChange).toFixed(2)}/month`,
          `Provider: ${formData.provider}`,
        ];
        break;
        
      case 'provider_migration':
        const percentage = parseFloat(formData.server_percentage) || 0;
        const fromProvider = formData.from_provider;
        const toProvider = formData.to_provider;
        
        if (!fromProvider || !toProvider || fromProvider === toProvider) {
          savings = 0;
          projectedCost = baselineCost;
          changePercent = 0;
          explanation = fromProvider === toProvider 
            ? 'Cannot migrate to the same provider. Please select different source and destination providers.'
            : 'Please select both source and destination providers.';
          details = ['Select different providers to see migration impact'];
        } else if (providerPricing[fromProvider] && providerPricing[toProvider]) {
          // Calculate based on actual provider pricing
          const fromCost = providerPricing[fromProvider].monthly;
          const toCost = providerPricing[toProvider].monthly;
          const costDiff = fromCost - toCost;
          const costDiffPercent = (costDiff / fromCost) * 100;
          
          // Estimate number of servers (assume ~10 servers for this dataset)
          const estimatedServers = 10;
          const serversToMigrate = Math.round(estimatedServers * (percentage / 100));
          const monthlySavingsPerServer = costDiff;
          const totalMonthlySavings = monthlySavingsPerServer * serversToMigrate;
          
          savings = totalMonthlySavings;
          projectedCost = baselineCost - savings;
          changePercent = -(savings / baselineCost) * 100;
          
          if (costDiff > 0) {
            explanation = `Migrating ${percentage}% of servers (${serversToMigrate} servers) from ${fromProvider} ($${fromCost}/server/month) to ${toProvider} ($${toCost}/server/month) will save $${monthlySavingsPerServer.toFixed(2)}/server/month, totaling $${savings.toFixed(2)}/month.`;
          } else {
            explanation = `Migrating ${percentage}% of servers (${serversToMigrate} servers) from ${fromProvider} ($${fromCost}/server/month) to ${toProvider} ($${toCost}/server/month) will increase costs by $${Math.abs(monthlySavingsPerServer).toFixed(2)}/server/month, totaling $${Math.abs(savings).toFixed(2)}/month additional cost.`;
          }
          
          details = [
            `From: ${fromProvider} ($${fromCost}/server/month) → To: ${toProvider} ($${toCost}/server/month)`,
            `Cost difference: ${costDiff > 0 ? '-' : '+'}$${Math.abs(costDiff).toFixed(2)}/server/month (${Math.abs(costDiffPercent).toFixed(1)}%)`,
            `Servers to migrate: ${serversToMigrate} (${percentage}% of fleet)`,
            `Monthly ${costDiff > 0 ? 'savings' : 'additional cost'}: $${Math.abs(savings).toFixed(2)}`,
            `Migration considerations: Downtime, data transfer costs, engineering effort`,
            `Estimated migration time: ${serversToMigrate <= 3 ? '1-2 weeks' : serversToMigrate <= 6 ? '3-4 weeks' : '1-2 months'}`,
          ];
        } else {
          // Fallback if pricing not available
          const avgSavingsPercent = 15;
          savings = (baselineCost * (percentage / 100) * (avgSavingsPercent / 100));
          projectedCost = baselineCost - savings;
          changePercent = -(savings / baselineCost) * 100;
          explanation = `Migrating ${percentage}% of servers from ${fromProvider} to ${toProvider} could save approximately $${savings.toFixed(2)}/month (estimated ${avgSavingsPercent}% cost reduction).`;
          details = [
            `From: ${fromProvider} → To: ${toProvider}`,
            `Servers to migrate: ${percentage}% of current fleet`,
            `Estimated savings: ${avgSavingsPercent}%`,
            `Note: Using estimated pricing. Actual costs may vary.`,
          ];
        }
        break;
        
      case 'traffic_growth':
        const growthPercent = parseFloat(formData.growth_percentage) || 0;
        const infrastructureScaling = growthPercent * 0.7; // 70% of traffic growth translates to infrastructure cost
        projectedCost = baselineCost * (1 + infrastructureScaling / 100);
        savings = -(projectedCost - baselineCost);
        changePercent = infrastructureScaling;
        explanation = `A ${growthPercent}% increase in traffic will require approximately ${infrastructureScaling.toFixed(1)}% more infrastructure, increasing monthly costs by $${Math.abs(savings).toFixed(2)}.`;
        details = [
          `Expected traffic growth: ${growthPercent}%`,
          `Infrastructure scaling factor: ${infrastructureScaling.toFixed(1)}%`,
          `Additional servers may be needed to maintain performance`,
          `Consider optimization initiatives to reduce scaling costs`,
        ];
        break;
        
      case 'cost_optimization':
        // Calculate savings from each optimization strategy
        let totalSavingsPercent = 0;
        const strategies = [];
        
        // Right-sizing savings
        if (formData.right_sizing && formData.right_sizing !== 'None') {
          let rightSizingPercent = 0;
          if (formData.right_sizing.includes('5-10%')) rightSizingPercent = 7.5;
          else if (formData.right_sizing.includes('10-15%')) rightSizingPercent = 12.5;
          else if (formData.right_sizing.includes('15-20%')) rightSizingPercent = 17.5;
          
          if (rightSizingPercent > 0) {
            totalSavingsPercent += rightSizingPercent;
            strategies.push(`Right-sizing: ${rightSizingPercent}% savings`);
          }
        }
        
        // Reserved instances savings (applied to base cost only)
        if (formData.reserved_instances && formData.reserved_instances !== 'None') {
          let reservedPercent = 0;
          if (formData.reserved_instances.includes('15%')) reservedPercent = 15;
          else if (formData.reserved_instances.includes('30%')) reservedPercent = 30;
          
          if (reservedPercent > 0) {
            // Reserved instances typically save 15-30% on compute costs (assume 60% of total)
            const effectiveSavings = reservedPercent * 0.6;
            totalSavingsPercent += effectiveSavings;
            strategies.push(`Reserved instances: ${effectiveSavings.toFixed(1)}% effective savings`);
          }
        }
        
        // Spot instances savings (applied to eligible workloads, assume 30% of infrastructure)
        if (formData.spot_instances && formData.spot_instances !== 'None') {
          let spotPercent = 0;
          if (formData.spot_instances.includes('20%')) spotPercent = 20;
          else if (formData.spot_instances.includes('40%')) spotPercent = 40;
          
          if (spotPercent > 0) {
            // Spot instances save 60-90% but only on ~30% of workloads
            const effectiveSavings = (spotPercent / 100) * 0.7 * 0.3 * 100; // 70% discount on 30% of workloads
            totalSavingsPercent += effectiveSavings;
            strategies.push(`Spot instances: ${effectiveSavings.toFixed(1)}% effective savings`);
          }
        }
        
        // Auto-scaling savings
        if (formData.auto_scaling && formData.auto_scaling !== 'None') {
          let autoScalingPercent = 0;
          if (formData.auto_scaling.includes('5-8%')) autoScalingPercent = 6.5;
          else if (formData.auto_scaling.includes('10-15%')) autoScalingPercent = 12.5;
          
          if (autoScalingPercent > 0) {
            totalSavingsPercent += autoScalingPercent;
            strategies.push(`Auto-scaling: ${autoScalingPercent}% savings`);
          }
        }
        
        // Calculate final numbers
        savings = baselineCost * (totalSavingsPercent / 100);
        projectedCost = baselineCost - savings;
        changePercent = -totalSavingsPercent;
        
        if (strategies.length === 0) {
          explanation = 'No optimization strategies selected. Choose at least one strategy to see potential savings.';
          details = ['Select optimization strategies from the dropdowns above'];
        } else {
          explanation = `Implementing ${strategies.length} optimization ${strategies.length === 1 ? 'strategy' : 'strategies'} will reduce monthly costs by approximately ${totalSavingsPercent.toFixed(1)}% ($${savings.toFixed(2)}/month).`;
          details = [
            ...strategies,
            `Combined savings: ${totalSavingsPercent.toFixed(1)}%`,
            `Monthly savings: $${savings.toFixed(2)}`,
            `Implementation effort: ${strategies.length <= 2 ? 'Low-Medium' : 'Medium-High'}`,
            `Timeline: ${strategies.length <= 2 ? '2-4 weeks' : '1-3 months'}`,
          ];
        }
        break;
        
      default:
        projectedCost = baselineCost;
        savings = 0;
        changePercent = 0;
        explanation = 'No changes calculated.';
        details = [];
    }
    
    const recommendation = savings > 0 ? 'Proceed' : savings < -1000 ? 'Caution' : 'Review';
    const rationale = savings > 0 
      ? `This scenario will save $${savings.toFixed(2)}/month. Recommended to proceed with implementation.`
      : savings < -1000
      ? `This scenario will increase costs by $${Math.abs(savings).toFixed(2)}/month. Carefully evaluate if the benefits justify the additional expense.`
      : `This scenario has minimal cost impact. Review whether it aligns with business objectives.`;
    
    const mockResult = {
      scenario_type: scenarioType,
      baseline: {
        total_cost: baselineCost,
      },
      projected: {
        total_cost: projectedCost,
        cost_change_percent: changePercent,
        savings: savings,
      },
      recommendation: recommendation,
      explanation: explanation,
      rationale: rationale,
      details: details,
    };
    
    setResult(mockResult);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl">
      <Typography variant="h4" gutterBottom>
        Scenario Studio
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
        Model what-if scenarios to optimize usage
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => {
          setActiveTab(newValue);
          setResult(null); // Clear results when switching tabs
        }}>
          {scenarios.map((scenario, index) => (
            <Tab key={index} label={scenario.title} />
          ))}
        </Tabs>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2" fontWeight="bold">{scenarios[activeTab].description}</Typography>
            <Typography variant="body2" sx={{ mt: 0.5 }}>{scenarios[activeTab].helpText}</Typography>
          </Alert>
        </Grid>
        <Grid item xs={12} md={6}>
          <ScenarioForm
            title={scenarios[activeTab].title}
            fields={scenarios[activeTab].fields}
            baseline={scenarios[activeTab].baseline}
            onSubmit={handleScenarioSubmit}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <ScenarioResult result={result} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default ScenarioStudio;
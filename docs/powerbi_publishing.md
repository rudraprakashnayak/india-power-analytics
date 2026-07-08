# Power BI Service Publishing Instructions

## Overview

This guide walks you through publishing your Power BI report to Power BI Service (app.powerbi.com) and generating a shareable link.

## Prerequisites

- Power BI Desktop installed and your .pbix report completed
- Free Power BI account (sign up at https://app.powerbi.com)
- Your report saved as `.pbix` file

## Step 1: Sign in to Power BI Desktop

1. Open your Power BI Desktop file
2. Click **Sign in** in the top right corner
3. Enter your Power BI account credentials
4. Wait for authentication to complete

## Step 2: Publish to Power BI Service

1. In Power BI Desktop, go to **Home** tab
2. Click **Publish** button (or press Ctrl+P)
3. A dialog will appear showing your workspaces
4. Select **My Workspace** (default for free accounts)
5. Click **Select**
6. Wait for the upload to complete (you'll see a success message)
7. Click the link in the success message to open the report in Power BI Service

## Step 3: Verify in Power BI Service

1. Your browser will open to app.powerbi.com
2. Navigate to **Workspaces** → **My Workspace**
3. You should see your report listed under **Reports**
4. Click on your report to open it
5. Verify all visuals, data, and interactivity work correctly

## Step 4: Generate Shareable Link (Publish to Web)

⚠️ **IMPORTANT WARNING**: "Publish to Web" makes your report **publicly accessible** to anyone with the link. This is suitable for:
- Synthetic/demo data (like this project)
- Public information
- Portfolio demonstrations

**DO NOT use Publish to Web for:**
- Confidential business data
- Personal information
- Sensitive metrics

### Option A: Publish to Web (Public Link)

1. With your report open in Power BI Service
2. Click **File** → **Publish to Web**
3. Read the warning dialog carefully
4. If you understand the risks, click **Create**
5. Configure settings:
   - **Embed code**: Choose how users can interact (can filter, can't edit data)
   - **Size**: Choose responsive or fixed size
6. Click **Copy Link**
7. Paste this link in your README.md

### Option B: Share with Specific Users (Requires Pro License)

If you have a Power BI Pro license (or your organization provides it):

1. With your report open in Power BI Service
2. Click **Share** button (top right)
3. Enter email addresses of people you want to share with
4. Set permissions (Can view, Can build)
5. Add an optional message
6. Click **Share**

**Note**: This requires recipients to have Power BI Pro licenses as well.

## Step 5: Embed in GitHub README

### Method 1: Direct Link (Publish to Web)

Add this to your README.md:

```markdown
## 🔗 Power BI Report

[View Interactive Report](https://app.powerbi.com/view?r=YOUR_REPORT_ID)

> ⚠️ **Note**: The interactive report is published using Power BI's "Publish to Web" feature, which makes the data publicly accessible. This is for demonstration purposes only with synthetic data.
```

### Method 2: Embed Code (Publish to Web)

Power BI also provides an embed code. Add to README.md:

```markdown
<iframe width="800" height="600" src="https://app.powerbi.com/reportEmbed?reportId=YOUR_REPORT_ID" frameborder="0" allowFullScreen="true"></iframe>
```

⚠️ **GitHub Note**: GitHub READMEs do not support iframes for security reasons. The embed code will not render directly on GitHub. Use the direct link instead.

## Step 6: Manage Published Reports

### To Update a Published Report

1. Make changes in Power BI Desktop
2. Save the .pbix file
3. Publish again (same process as Step 2)
4. Power BI will ask if you want to replace the existing report
5. Click **Replace**
6. The link remains the same, but content updates

### To Unpublish/Delete

1. Go to Power BI Service
2. Navigate to **Workspaces** → **My Workspace**
3. Find your report
4. Click the **...** (more options) menu
5. Select **Delete**
6. Confirm deletion

## Step 7: Set Visibility and Access Control

### For Free Accounts

- Only **Publish to Web** is available for public sharing
- No access control - anyone with the link can view
- Report remains in your workspace

### For Pro/Premium Accounts

Additional options available:
- **Row-Level Security**: Restrict data visibility by user
- **Workspaces**: Collaborate with teams
- **Apps**: Package reports for distribution
- **Gateways**: Connect to on-premises data sources

## Best Practices for Portfolio Projects

1. **Use Synthetic Data**: Always use fake/demo data for portfolio projects
2. **Document Public Access**: Clearly state in README that data is synthetic
3. **Monitor Access**: Periodically check who is accessing your published reports
4. **Update Regularly**: Keep reports updated with your latest work
5. **Consider Alternatives**: For sensitive projects, use screenshots instead of live reports

## Troubleshooting

### Publish Fails
- Check your internet connection
- Verify you're signed in to Power BI Desktop
- Ensure your .pbix file is not corrupted (try opening it again)

### Link Doesn't Work
- Verify the link was copied correctly
- Check if you're signed in to Power BI Service
- Try opening in an incognito/private browser window

### Report Shows Blank
- Check if data sources are accessible
- Verify data model relationships
- Refresh the report in Power BI Service

## Security Considerations

**Publish to Web Risks:**
- Anyone with the link can view the report
- Search engines may index the report
- No access control or authentication
- Data is publicly accessible

**Recommendations:**
- Only use with synthetic/demo data
- Add disclaimer in your README
- Monitor link sharing
- Consider using screenshots for sensitive projects
- Delete published reports when no longer needed

---

## Summary Checklist

- [ ] Sign in to Power BI Desktop
- [ ] Publish report to Power BI Service
- [ ] Verify report in browser
- [ ] Generate Publish to Web link (if using synthetic data)
- [ ] Copy link to clipboard
- [ ] Add link to README.md
- [ ] Test link in incognito window
- [ ] Document data source as synthetic in README

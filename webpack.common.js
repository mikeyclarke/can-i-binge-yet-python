const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const WebpackAssetsManifest = require('webpack-assets-manifest');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const fs = require('fs');

const applicationConfig = fs.readFileSync('./config/application.py', 'utf8');
const appConfigLines = applicationConfig.split(/\r?\n/);

let snowfall = false;
appConfigLines.forEach((line) => {
    if (line.startsWith('SNOWFALL')) {
        const value = line.match(/SNOWFALL\s=\s([A-Za-z]+)$/);
        if (null !== value) {
            snowfall = (value[1].toLowerCase() === 'true') ? true : false;
        }
    }
});

module.exports = {
    entry: {
        app: ['./src/ts/app.ts', './ui/sass/app.scss'],
    },
    output: {
        path: path.resolve(__dirname, 'public/compiled'),
        publicPath: '/compiled/',
        filename: '[name].[contenthash].js',
        chunkFilename: '[name].[contenthash].js',
        crossOriginLoading: 'anonymous',
    },
    stats: {
        children: false,
        modulesSpace: 0,
    },
    plugins: [
        new CleanWebpackPlugin(),
        new WebpackAssetsManifest({
            publicPath: true,
            output: 'manifest.json',
        }),
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css',
        }),
    ],
    resolve: {
        extensions: ['.ts'],
        modules: [
            path.resolve('./src/ts'),
        ],
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: [
                    'ts-loader',
                ],
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            additionalData: '$snowfall: ' + snowfall + ';',
                            webpackImporter: false,
                            sassOptions: {
                                includePaths: ['./ui/sass', './node_modules']
                            },
                        },
                    },
                ],
            },
        ],
    },
    optimization: {
        minimizer: [
            new CssMinimizerPlugin({
                minimizerOptions: {
                    preset: [
                        'default',
                        {
                            discardUnused: true,
                            mergeIdents: true,
                        }
                    ],
                },
            }),
        ],
        splitChunks: false,
    },
};
